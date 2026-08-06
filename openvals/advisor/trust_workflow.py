from datetime import datetime
from pathlib import Path
import time

from openvals.utils.system import get_system_profile

from openvals.advisor.modes import MODES
from openvals.advisor.trust_profile import build_trust_profile
from openvals.advisor.trust_readiness import compute_trust_readiness
from openvals.advisor.trust_verdict import generate_trust_verdict

from openvals.datasets.loader import load_builtin_dataset
from openvals.datasets.metadata import load_dataset_metadata
from openvals.config.loader import load_config

from openvals.models.ollama_model import OllamaModel
from openvals.models.availability import (
    is_ollama_model_available,
    pull_ollama_model,
)

from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.recommendation.engine import RecommendationEngine

from openvals.reporting.html_report import generate_html_report
from openvals.reporting.sample_report import generate_sample_report


# =========================================================
# TRUST WORKFLOW
# =========================================================

def run_trust_workflow(
    problem_text,
    top_k=3,
    dataset=None,
    config=None,
    parallel=True,
    max_workers=None,
    auto_pull=False,
    explain=False,
    mode="standard",
    generate_reports=True,
    output_dir="outputs",
):
    """
    Run the complete OpenVals trust workflow.

    The workflow:

    1. Builds the trust profile.
    2. Calculates the Trust Readiness Index.
    3. Selects models based on benchmark mode.
    4. Detects system capacity and worker count.
    5. Checks model availability.
    6. Loads the selected dataset and metric weights.
    7. Runs the benchmark.
    8. Determines the best model and DRS.
    9. Generates the final trust verdict.
    10. Generates executive and sample-level HTML reports.
    """

    workflow_start_time = datetime.now()
    workflow_start_perf = time.perf_counter()

    mode_cfg = MODES.get(
        mode,
        MODES["standard"],
    )

    if explain:
        print(
            "\n====> OpenVals Trust WorkFlow Started <===="
        )
        print(
            f"Start Time: {workflow_start_time}"
        )

        print("\nBenchmark Mode")
        print(f"Mode        : {mode}")
        print(
            f"Description : "
            f"{mode_cfg.get('description', '')}"
        )

    # =====================================================
    # TRUST PROFILE
    # =====================================================

    profile = build_trust_profile(
        problem_text,
        top_k=top_k,
    )

    if explain:
        print(
            "\n===== Recommended Profile ====="
        )

        for model in profile.get(
            "recommended_models",
            [],
        ):
            print(
                f"Recommended: {model['model']}"
            )

        print("===============================")

    # =====================================================
    # TRUST READINESS INDEX
    # =====================================================

    tri = compute_trust_readiness(
        profile
    )

    # =====================================================
    # DATASET + CONFIG
    # =====================================================

    selected_dataset = (
        dataset
        or profile.get("recommended_dataset")
    )

    selected_config = (
        config
        or profile.get("recommended_config")
    )

    # =====================================================
    # MODEL SELECTION
    # =====================================================

    model_names = [
        model["model"]
        for model in profile.get(
            "recommended_models",
            [],
        )
    ]

    mode_top_k = mode_cfg.get("top_k")

    if mode_top_k:
        model_names = model_names[:mode_top_k]

        if explain:
            print(
                f"\nModel limit applied: "
                f"top {mode_top_k} models"
            )

            print(
                "\nModels selected for benchmark:"
            )

            for model_name in model_names:
                print(f"→ {model_name}")

    # =====================================================
    # SYSTEM PROFILE + WORKERS
    # =====================================================

    system_profile = get_system_profile(
        mode=mode,
        model_count=len(model_names),
    )

    recommended_workers = system_profile[
        "recommended_max_workers"
    ]

    if max_workers is None:
        max_workers = recommended_workers
        worker_source = "auto-recommended"
    else:
        worker_source = "user-specified"

    if explain:
        print(
            "\n====> System Profile <===="
        )
        print(
            f"CPU Cores           : "
            f"{system_profile.get('cpu_count')}"
        )
        print(
            f"Memory GB           : "
            f"{system_profile.get('memory_gb')}"
        )
        print(
            f"Recommended Workers : "
            f"{recommended_workers}"
        )
        print(
            f"Selected Workers    : "
            f"{max_workers}"
        )
        print(
            f"Worker Source       : "
            f"{worker_source}"
        )

    # =====================================================
    # LOAD MODELS
    # =====================================================

    loaded_models = {}
    skipped_models = []

    if explain:
        print(
            "\n====> Checking Recommended "
            "Model Availability <===="
        )

    for model_name in model_names:
        if explain:
            print(
                f"🔎 Checking model: {model_name}"
            )

        if not is_ollama_model_available(
            model_name
        ):
            if auto_pull:
                if explain:
                    print(
                        f"Attempting to pull model: "
                        f"{model_name}"
                    )

                pulled = pull_ollama_model(
                    model_name
                )

                if not pulled:
                    skipped_models.append(
                        model_name
                    )

                    if explain:
                        print(
                            f"⚠ Skipping unavailable "
                            f"model: {model_name}"
                        )

                    continue

            else:
                skipped_models.append(
                    model_name
                )

                if explain:
                    print(
                        f"⚠ Skipping unavailable "
                        f"model: {model_name}"
                    )

                continue

        try:
            loaded_models[model_name] = (
                OllamaModel(model_name)
            )

            if explain:
                print(
                    f"✅ Model loaded: "
                    f"{model_name}"
                )

        except Exception as error:
            skipped_models.append(
                model_name
            )

            if explain:
                print(
                    f"⚠ Model could not be loaded: "
                    f"{model_name}"
                )
                print(
                    f"Reason: {error}"
                )

    # =====================================================
    # NO MODELS AVAILABLE
    # =====================================================

    if not loaded_models:
        trust_verdict = generate_trust_verdict(
            tri_score=tri["tri_score"],
            drs_score=0.0,
            risk_level=profile["risk_level"],
            data_sensitivity=profile[
                "data_sensitivity"
            ],
        )

        timing = build_timing(
            workflow_start_time,
            workflow_start_perf,
        )

        return {
            "profile": profile,
            "tri": tri,
            "benchmark_results": {},
            "best_model": None,
            "best_drs": 0.0,
            "trust_verdict": trust_verdict,
            "recommendation": None,
            "reports": {
                "executive": None,
                "sample": None,
            },
            "dataset": selected_dataset,
            "config": selected_config,
            "recommended_models": [
                model["model"]
                for model in profile.get(
                    "recommended_models",
                    [],
                )
            ],
            "benchmark_models": model_names,
            "loaded_models": [],
            "skipped_models": skipped_models,
            "recommended_workers": (
                recommended_workers
            ),
            "worker_source": worker_source,
            "max_workers": max_workers,
            "sample_limit": mode_cfg.get(
                "sample_limit"
            ),
            "mode": mode,
            "mode_config": mode_cfg,
            "system_profile": system_profile,
            "timing": timing,
        }

    # =====================================================
    # LOAD DATASET
    # =====================================================

    try:
        dataset_data = load_builtin_dataset(
            selected_dataset
        )

    except Exception as error:
        if explain:
            print(
                f"\n⚠ Dataset not found: "
                f"{selected_dataset}"
            )
            print(
                f"Reason: {error}"
            )
            print(
                "Using fallback dataset: finance"
            )

        selected_dataset = "finance"
        selected_config = "finance"

        dataset_data = load_builtin_dataset(
            selected_dataset
        )

    sample_limit = mode_cfg.get(
        "sample_limit"
    )

    if sample_limit:
        dataset_data = dataset_data[
            :sample_limit
        ]

        if explain:
            print(
                f"Dataset samples selected: "
                f"{len(dataset_data)}"
            )

    # =====================================================
    # LOAD METRIC WEIGHTS
    # =====================================================

    try:
        if selected_config:
            cfg = load_config(
                selected_config
            )

            weights = cfg["weights"]

        else:
            metadata = load_dataset_metadata(
                selected_dataset
            )

            weights = metadata[
                "recommended_weights"
            ]

    except Exception as error:
        if explain:
            print(
                f"\n⚠ Could not load config: "
                f"{selected_config}"
            )
            print(
                f"Reason: {error}"
            )
            print(
                "Using dataset metadata weights."
            )

        metadata = load_dataset_metadata(
            selected_dataset
        )

        weights = metadata[
            "recommended_weights"
        ]

        selected_config = "metadata_default"

    # =====================================================
    # RUN BENCHMARK
    # =====================================================

    runner = BenchmarkRunner(
        models=loaded_models,
        dataset=dataset_data,
        weights=weights,
        debug=False,
        parallel=parallel,
        max_workers=max_workers,
        verbose=explain,
    )

    if explain:
        print(
            "\n====> Running Benchmarking <===="
        )

    benchmark_results = runner.run()

    # =====================================================
    # BEST MODEL
    # =====================================================

    ranking = sorted(
        benchmark_results.items(),
        key=lambda item: item[1].get(
            "drs_score",
            0,
        ),
        reverse=True,
    )

    if ranking:
        best_model = ranking[0][0]

        best_drs = ranking[0][1].get(
            "drs_score",
            0,
        )

    else:
        best_model = None
        best_drs = 0.0

    # =====================================================
    # RECOMMENDATION ENGINE
    # =====================================================

    recommendation = None

    if benchmark_results:
        try:
            recommendation_engine = (
                RecommendationEngine(
                    benchmark_results
                )
            )

            recommendation = (
                recommendation_engine.recommend(
                    use_case=selected_dataset
                )
            )

        except Exception as error:
            if explain:
                print(
                    "\n⚠ Recommendation engine "
                    "could not complete."
                )
                print(
                    f"Reason: {error}"
                )

            recommendation = (
                build_fallback_recommendation(
                    best_model=best_model,
                    best_drs=best_drs,
                )
            )

    # =====================================================
    # FINAL TRUST VERDICT
    # =====================================================

    trust_verdict = generate_trust_verdict(
        tri_score=tri["tri_score"],
        drs_score=best_drs,
        risk_level=profile["risk_level"],
        data_sensitivity=profile[
            "data_sensitivity"
        ],
    )

    # =====================================================
    # TIMING
    # =====================================================

    timing = build_timing(
        workflow_start_time,
        workflow_start_perf,
    )

    # =====================================================
    # GENERATE REPORTS
    # =====================================================

    reports = {
        "executive": None,
        "sample": None,
    }

    if (
        generate_reports
        and benchmark_results
    ):
        output_directory = Path(
            output_dir
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        executive_report_path = (
            output_directory
            / (
                f"trust_report_"
                f"{selected_dataset}.html"
            )
        )

        sample_report_path = (
            output_directory
            / (
                f"sample_report_"
                f"{selected_dataset}.html"
            )
        )

        try:
            generate_html_report(
                results=benchmark_results,
                recommendation=recommendation,
                output_file=str(
                    executive_report_path
                ),
                dataset_name=selected_dataset,
                config_name=selected_config,
            )

            reports["executive"] = str(
                executive_report_path.resolve()
            )

        except Exception as error:
            if explain:
                print(
                    "\n⚠ Executive report generation "
                    "failed."
                )
                print(
                    f"Reason: {error}"
                )

        try:
            generate_sample_report(
                results=benchmark_results,
                output_file=str(
                    sample_report_path
                ),
            )

            reports["sample"] = str(
                sample_report_path.resolve()
            )

        except Exception as error:
            if explain:
                print(
                    "\n⚠ Sample report generation "
                    "failed."
                )
                print(
                    f"Reason: {error}"
                )

        if explain:
            print(
                "\n====> Report Generation <===="
            )

            if reports["executive"]:
                print(
                    f"Executive Report : "
                    f"{reports['executive']}"
                )

            if reports["sample"]:
                print(
                    f"Sample Report    : "
                    f"{reports['sample']}"
                )

            if not any(reports.values()):
                print(
                    "No reports were generated."
                )

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {
        "profile": profile,
        "tri": tri,
        "benchmark_results": (
            benchmark_results
        ),
        "best_model": best_model,
        "best_drs": best_drs,
        "trust_verdict": trust_verdict,
        "recommendation": recommendation,
        "reports": reports,
        "dataset": selected_dataset,
        "config": selected_config,
        "recommended_models": [
            model["model"]
            for model in profile.get(
                "recommended_models",
                [],
            )
        ],
        "benchmark_models": model_names,
        "loaded_models": list(
            loaded_models.keys()
        ),
        "skipped_models": skipped_models,
        "recommended_workers": (
            recommended_workers
        ),
        "worker_source": worker_source,
        "max_workers": max_workers,
        "sample_limit": sample_limit,
        "mode": mode,
        "mode_config": mode_cfg,
        "system_profile": system_profile,
        "timing": timing,
    }


# =========================================================
# FALLBACK RECOMMENDATION
# =========================================================

def build_fallback_recommendation(
    best_model,
    best_drs,
):
    """
    Build a minimal recommendation if the normal recommendation
    engine cannot complete.
    """

    return {
        "recommended_model": (
            best_model or "Unknown"
        ),
        "score": best_drs,
        "drs": best_drs,
        "confidence": best_drs,
        "reason": (
            "Selected using the highest available "
            "Decision Reliability Score."
        ),
        "tradeoffs": (
            "Additional domain-specific validation "
            "may be required."
        ),
        "risks": [],
        "insights": [],
        "deployment": {
            "readiness": "Unknown",
            "recommendations": [],
            "risks": [],
        },
    }


# =========================================================
# BUILD TIMING
# =========================================================

def build_timing(
    start_time,
    start_perf,
):
    """
    Build consistent workflow timing metadata.
    """

    end_time = datetime.now()

    duration_seconds = round(
        time.perf_counter() - start_perf,
        3,
    )

    duration_minutes = round(
        duration_seconds / 60,
        2,
    )

    return {
        "start_time": str(start_time),
        "end_time": str(end_time),
        "duration_seconds": duration_seconds,
        "duration_minutes": duration_minutes,
        "duration_human": format_duration(
            duration_seconds
        ),
    }


# =========================================================
# FORMAT DURATION
# =========================================================

def format_duration(seconds):
    seconds = int(seconds)

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes == 0:
        return f"{remaining_seconds}s"

    return (
        f"{minutes}m "
        f"{remaining_seconds}s"
    )
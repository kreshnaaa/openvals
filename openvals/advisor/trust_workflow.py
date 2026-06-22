from datetime import datetime
import time

from openvals.utils.system import get_system_profile

from openvals.advisor.modes import MODES

from openvals.advisor.trust_profile import (
    build_trust_profile
)

from openvals.advisor.trust_readiness import (
    compute_trust_readiness
)

from openvals.advisor.trust_verdict import (
    generate_trust_verdict
)

from openvals.datasets.loader import (
    load_builtin_dataset
)

from openvals.datasets.metadata import (
    load_dataset_metadata
)

from openvals.config.loader import (
    load_config
)

from openvals.models.ollama_model import (
    OllamaModel
)

from openvals.benchmarking.benchmark import (
    BenchmarkRunner
)

from openvals.models.availability import (
    is_ollama_model_available,
    pull_ollama_model
)

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
    mode="standard"

):

    workflow_start_time = datetime.now()
    workflow_start_perf = time.perf_counter()

    mode_cfg = MODES.get(
        mode,
        MODES["standard"]
    )
    if explain:
        print("\n====> OpenVals Trust WorkFlow Started <====")
        print(f"Start Time: {workflow_start_time}")
        print("\nBenchmark Mode")
        print(f"Mode        : {mode}")
        print(f"Description : {mode_cfg.get('description', '')}")
    # =====================================================
    # TRUST PROFILE
    # =====================================================
    profile = build_trust_profile(
        problem_text,
        top_k=top_k
    )
    if explain:
        print("\n===== Recommended Profile =====")
        for model in profile.get("recommended_models", []):
            print(f"Recommended: {model['model']}")
    print("=========================")
    # =====================================================
    # TRI
    # =====================================================

    tri = compute_trust_readiness(
        profile
    )

    # =====================================================
    # DATASET + CONFIG
    # =====================================================

    selected_dataset = dataset or profile.get(
        "recommended_dataset"
    )

    selected_config = config or profile.get(
        "recommended_config"
    )

    # =====================================================
    # MODELS
    # =====================================================

    model_names = [
        model["model"]
        for model in profile.get(
            "recommended_models",
            []
        )
    ]

    mode_top_k = mode_cfg.get(
        "top_k"
    )
    
    if mode_top_k:
        model_names = model_names[
            :mode_top_k
        ]
        if explain:
            print(f"\nModel limit applied: top {mode_top_k} models")
            print("\n Models selected for benchmark:")
            for model_name in model_names:
                print(f"→ {model_name}")
    # =====================================================
    # SYSTEM PROFILE + WORKERS
    # =====================================================

    system_profile = get_system_profile(
        mode=mode,
        model_count=len(model_names)
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
        print("\n====> System Profile <====")
        print(f"CPU Cores        : {system_profile.get('cpu_count')}")
        print(f"Memory GB        : {system_profile.get('memory_gb')}")
        print(f"Recommended Workers : {recommended_workers}")
        print(f"Selected Workers    : {max_workers}")
        print(f"Worker Source       : {worker_source}")
    # =====================================================
    # LOAD MODELS
    # =====================================================
    loaded_models = {}
    skipped_models = []
    if explain:
        print("\n====>\nChecking recommended model availability...<====")
    for model_name in model_names:
        if explain:
            print(f" Checking model: {model_name}")
        if not is_ollama_model_available(
            model_name
        ):
            if auto_pull:
                if explain:
                    print(f" Attempting to pull model from Ollama: {model_name}")
                pulled = pull_ollama_model(
                    model_name
                )
                if not pulled:
                    skipped_models.append(
                        model_name)
                    if explain:
                        print(f"⚠ Skipping unavailable model: {model_name}")
                    continue
            else:
                skipped_models.append(
                    model_name
                )
                if explain:
                    print(f"⚠ Skipping unavailable model: {model_name}")
                continue
        try:
            loaded_models[
                model_name
            ] = OllamaModel(
                model_name
            )
            if explain:
                print(f"Model {model_name} loaded successfully.")
        except Exception as e:
            skipped_models.append(
                model_name
            )
            if explain:
                print(f"Model {model_name} could not be loaded. ⚠ Skipping.")
    if not loaded_models:
        trust_verdict = generate_trust_verdict(
            tri_score=tri["tri_score"],
            drs_score=0.0,
            risk_level=profile["risk_level"],
            data_sensitivity=profile["data_sensitivity"]
        )

        workflow_end_time = datetime.now()
        workflow_end_perf = time.perf_counter()

        duration_seconds = round(
            workflow_end_perf - workflow_start_perf,
            3
        )

        duration_minutes = round(
            duration_seconds / 60,
            2
        )

        duration_human = format_duration(
            duration_seconds
        )

        return {
            "profile": profile,
            "tri": tri,
            "benchmark_results": {},
            "best_model": None,
            "best_drs": 0.0,
            "trust_verdict": trust_verdict,
            "dataset": selected_dataset,
            "config": selected_config,
            "recommended_models": [
                model["model"]
                for model in profile.get(
                    "recommended_models",
                    []
                )
            ],
            "benchmark_models": model_names,
            "loaded_models": list(
                loaded_models.keys()
            ),
            "skipped_models": skipped_models,
            "recommended_workers": recommended_workers,
            "worker_source": worker_source,
            "max_workers": max_workers,
            "sample_limit": mode_cfg.get("sample_limit"),
            "mode": mode,
            "mode_config": mode_cfg,
            "system_profile": system_profile,
            "timing": {
                "start_time": str(workflow_start_time),
                "end_time": str(workflow_end_time),
                "duration_seconds": duration_seconds,
                "duration_minutes": duration_minutes,
                "duration_human": duration_human
            }
        }

    # =====================================================
    # LOAD DATASET
    # =====================================================
    try:
        dataset_data = load_builtin_dataset(
            selected_dataset
        )
    except Exception:
        if explain:
            print(f"\n⚠ Dataset not found: {selected_dataset}")
            print("Using fallback dataset: finance")
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
    # =====================================================
    # LOAD WEIGHTS
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
    except Exception:
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
        verbose=explain
    )
    if explain:
        print("\n====> Running Benchmarking... <====")
    benchmark_results = runner.run()


    # =====================================================
    # BEST MODEL
    # =====================================================

    ranking = sorted(
        benchmark_results.items(),
        key=lambda x: x[1].get(
            "drs_score",
            0
        ),
        reverse=True
    )

    if ranking:

        best_model = ranking[0][0]

        best_drs = ranking[0][1].get(
            "drs_score",
            0
        )

    else:

        best_model = None
        best_drs = 0.0

    # =====================================================
    # FINAL VERDICT
    # =====================================================

    trust_verdict = generate_trust_verdict(
        tri_score=tri["tri_score"],
        drs_score=best_drs,
        risk_level=profile["risk_level"],
        data_sensitivity=profile["data_sensitivity"]
    )

    workflow_end_time = datetime.now()
    workflow_end_perf = time.perf_counter()

    duration_seconds = round(
        workflow_end_perf - workflow_start_perf,
        3
    )

    duration_minutes = round(
        duration_seconds / 60,
        2
    )

    duration_human = format_duration(
        duration_seconds
    )
    return {
        "profile": profile,
        "tri": tri,
        "benchmark_results": benchmark_results,
        "best_model": best_model,
        "best_drs": best_drs,
        "trust_verdict": trust_verdict,
        "dataset": selected_dataset,
        "config": selected_config,
        "recommended_models": [
            model["model"]
            for model in profile.get(
                "recommended_models",
                []
            )
        ],
        "benchmark_models": model_names,
        "loaded_models": list(
            loaded_models.keys()
        ),
        "skipped_models": skipped_models,
        "recommended_workers": recommended_workers,
        "worker_source": worker_source,
        "max_workers": max_workers,
        "sample_limit": mode_cfg.get("sample_limit"),
        "mode": mode,
        "mode_config": mode_cfg,
        "system_profile": system_profile,
        "timing": {
            "start_time": str(workflow_start_time),
            "end_time": str(workflow_end_time),
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_minutes,
            "duration_human": duration_human
        }
    }


# =========================================================
# FORMAT DURATION
# =========================================================

def format_duration(seconds):

    seconds = int(
        seconds
    )

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes == 0:

        return f"{remaining_seconds}s"

    return (
        f"{minutes}m "
        f"{remaining_seconds}s"
    )
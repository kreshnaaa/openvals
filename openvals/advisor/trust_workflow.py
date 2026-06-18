import profile

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
print("\n ====>TRUST WORKFLOW STARTED<====\n") #remove this after debugging
def run_trust_workflow(
    problem_text,
    top_k=3,
    dataset=None,
    config=None,
    parallel=True,
    max_workers=2,
    debug=False,
    auto_pull=False,
    quick=False
):

    # =====================================================
    # TRUST PROFILE
    # =====================================================

    profile = build_trust_profile(
        problem_text,
        top_k=top_k
    )
    print("\n===== TRUST PROFILE =====")
    for model in profile["recommended_models"]:
        print(f"Recommended: {model['model']}")
    print("=========================\n")

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
    if quick:

        model_names = model_names[:2]

        print("\n⚡ QUICK MODE ENABLED")
        print("Using top 2 recommended models")

    print("\n Models recommended for benchmarking:")

    for model_name in model_names:
        print(
            f"→ {model_name}"
        )

    loaded_models = {}
    skipped_models = []

    print("\nChecking recommended model availability...")

    for model_name in model_names:

        print(
            f"🔎 Checking model: {model_name}"
        )

        if not is_ollama_model_available(
            model_name
        ):

            print(
                f"⚠ Skipping unavailable model: {model_name}"
            )

            skipped_models.append(
                model_name
            )

            continue

        try:

            loaded_models[
                model_name
            ] = OllamaModel(
                model_name
            )

            print(
                f"✅ Loaded recommended model: {model_name}"
            )

        except Exception as e:

            print(
                f"⚠ Failed to load model {model_name}: {str(e)}"
            )

            skipped_models.append(
                model_name
            )

    if not loaded_models:

        return {
            "profile": profile,
            "tri": tri,
            "benchmark_results": {},
            "best_model": None,
            "best_drs": 0.0,
            "trust_verdict": generate_trust_verdict(
                tri_score=tri["tri_score"],
                drs_score=0.0,
                risk_level=profile["risk_level"],
                data_sensitivity=profile["data_sensitivity"]
            )
        }

    # =====================================================
    # LOAD DATASET
    # =====================================================

    dataset_data = load_builtin_dataset(
        selected_dataset
    )
    if quick:
        dataset_data = dataset_data[:3]
        print(f"Using {len(dataset_data)} samples")

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
        debug=debug,
        parallel=parallel,
        max_workers=max_workers
    )

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

    return {
        "profile": profile,
        "tri": tri,
        "benchmark_results": benchmark_results,
        "best_model": best_model,
        "best_drs": best_drs,
        "trust_verdict": trust_verdict,
        "dataset": selected_dataset,
        "skipped_models": skipped_models,
        "config": selected_config
    }
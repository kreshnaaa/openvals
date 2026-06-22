def print_trust_workflow_explanation(workflow):

    profile = workflow.get("profile", {})
    tri = workflow.get("tri", {})
    verdict = workflow.get("trust_verdict", {})
    timing = workflow.get("timing", {})
    system = workflow.get("system_profile", {})
    mode_config = workflow.get("mode_config", {})

    recommended_models = workflow.get(
        "recommended_models",
        []
    )

    benchmark_models = workflow.get(
        "benchmark_models",
        []
    )

    loaded_models = workflow.get(
        "loaded_models",
        []
    )

    skipped_models = workflow.get(
        "skipped_models",
        []
    )

    print("\n=====> OpenVals Trust Advisor Report <=====\n")

    print("\nProvided Profile")
    print(f"Use Case         : {profile.get('use_case')}")
    print(f"Risk Level       : {profile.get('risk_level')}")
    print(f"Data Sensitivity : {profile.get('data_sensitivity')}")
    print(f"Dataset          : {workflow.get('dataset')}")
    print(f"Config           : {workflow.get('config')}")

    print("\nTrust Readiness")
    print(f"TRI Score        : {tri.get('tri_score')}/100")
    print(f"Readiness        : {tri.get('readiness')}")

    print("\nBenchmark Plan")
    print(f"Mode             : {workflow.get('mode')}")
    print(f"Description      : {mode_config.get('description')}")
    print(f"Sample Limit     : {workflow.get('sample_limit')}")
    print(f"Recommended Count: {len(recommended_models)}")
    print(f"Benchmark Count  : {len(benchmark_models)}")

    print("\nRecommended Models")
    for model in recommended_models:
        print(f"→ {model}")

    print("\nSelected for Benchmark")
    for model in benchmark_models:
        print(f"→ {model}")

    print("\nSystem Recommendation")
    print(f"CPU Cores        : {system.get('cpu_count')}")
    print(f"Memory GB        : {system.get('memory_gb')}")
    print(f"Recommended Workers : {workflow.get('recommended_workers')}")
    print(f"Selected Workers    : {workflow.get('max_workers')}")
    print(f"Worker Source       : {workflow.get('worker_source')}")

    print("\nModel Availability")
    if loaded_models:
        print(f"Loaded Models    : {len(loaded_models)}")
        for model in loaded_models:
            print(f"✅ {model}")

    if skipped_models:
        print(f"Skipped Models   : {len(skipped_models)}")
        for model in skipped_models:
            print(f"⚠ {model}")

    benchmark_results = workflow.get(
        "benchmark_results",
        {}
    )

    if benchmark_results:

        best_drs_percent = round(
            workflow.get("best_drs", 0) * 100,
            1
        )

        print("\nBenchmark Result")
        print(f"Best Model       : {workflow.get('best_model')}")
        print(f"Best DRS         : {best_drs_percent}%")

    print("\nTrust Verdict")
    print(f"Verdict          : {verdict.get('verdict')}")
    print(f"Recommendation   : {verdict.get('recommendation')}")

    controls = verdict.get(
        "required_controls",
        []
    )

    if controls:
        print("\nRequired Controls")
        for control in controls:
            print(f"→ {control}")

    print("\nTiming")
    print(f"Duration         : {timing.get('duration_human')}")
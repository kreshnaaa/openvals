import typer
from pathlib import Path

from openvals import __version__

from openvals.datasets.loader import (
    load_builtin_dataset
)

from openvals.datasets.metadata import (
    load_dataset_metadata
)

from openvals.datasets.registry import (
    DATASETS
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

from openvals.recommendation.engine import (
    RecommendationEngine
)

from openvals.reporting.html_report import (
    generate_html_report
)

from openvals.utils.paths import (
    create_output_structure
)

# =========================================================
# TYPER APP
# =========================================================

app = typer.Typer(

    help=
    "OpenVals - AI Evaluation & "
    "Trust Intelligence Framework"

)

# =========================================================
# VERSION
# =========================================================

@app.command()
def version():

    """
    Show OpenVals version.
    """

    typer.echo(

        f"OpenVals v{__version__} "
        f"built by DrPinnacle "
        f"(https://drpinnacle.com) "
        f"Vishwanath Akuthota"

    )

# =========================================================
# BENCHMARK
# =========================================================

@app.command("benchmark")
def benchmark(

    dataset: str = typer.Option(
        ...,
        help="Dataset name"
    ),

    config: str = typer.Option(
        None,
        help="Config preset"
    ),

    models: str = typer.Option(
        ...,
        help="Comma-separated model names"
    ),

    report: bool = typer.Option(
        True,
        help="Generate HTML report"
    ),

    output: str = typer.Option(
        "outputs/report.html",
        help="Output HTML report file"
    )

):

    """
    Run OpenVals benchmark.
    """
    typer.echo(

        f"\n🚀 OpenVals AI Trust Platform "
        f"Starting... (v{__version__})\n"

    )
    # =====================================================
    # CREATE OUTPUT STRUCTURE
    # =====================================================
    create_output_structure()
    output_path = Path(output)
    if not output_path.parent.exists():
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
    # =====================================================
    # LOAD DATASET
    # =====================================================
    dataset_data = load_builtin_dataset(
        dataset
    )

    metadata = load_dataset_metadata(
        dataset
    )

    if config:

        cfg = load_config(config)

        weights = cfg["weights"]

        typer.echo(
            f"⚙️ Config Loaded : {config}"
        )

    else:

        weights = metadata[
            "recommended_weights"
        ]

    typer.echo("📦 Dataset Loaded")

    typer.echo(
        f"Dataset : {metadata['name']}"
    )

    typer.echo(
        f"Domain  : {metadata['domain']}"
    )

    typer.echo(
        f"Version : {metadata['version']}\n"
    )

    # =====================================================
    # LOAD MODELS
    # =====================================================

    model_names = [

        m.strip()

        for m in models.split(",")

    ]

    loaded_models = {}

    for model_name in model_names:

        try:

            loaded_models[
                model_name
            ] = OllamaModel(model_name)

        except Exception as e:

            typer.echo(

                f"❌ Failed to load model "
                f"{model_name}: {str(e)}"

            )

    if not loaded_models:

        typer.echo(
            "\n❌ No models loaded successfully."
        )

        raise typer.Exit()

    typer.echo(

        f"🤖 Models Loaded: "
        f"{', '.join(loaded_models.keys())}\n"

    )

    # =====================================================
    # RUN BENCHMARK
    # =====================================================

    runner = BenchmarkRunner(

        models=loaded_models,
        dataset=dataset_data,
        weights=weights,
        debug=False

    )

    results = runner.run()

    # =====================================================
    # DRS RANKING
    # =====================================================

    ranking = sorted(

        [

            (
                model_name,
                results[model_name][
                    "drs_score"
                ]
            )

            for model_name in results

        ],

        key=lambda x: x[1],
        reverse=True

    )

    # =====================================================
    # FINAL TABLE
    # =====================================================

    typer.echo(

        "\n=== MODEL BENCHMARK "
        "(DRS Ranked) ===\n"

    )

    print(

        f"{'Rank':<5} "
        f"{'Model':<15} "
        f"{'Acc':<8} "
        f"{'Sem':<8} "
        f"{'Fact':<8} "
        f"{'Rel':<8} "
        f"{'Safe':<8} "
        f"{'Cons':<8} "
        f"{'Var':<8} "
        f"{'HPI':<8} "
        f"{'Lat(ms)':<12} "
        f"{'DRS':<8}"

    )

    print("-" * 140)

    for rank, (

        model_name,
        drs_score

    ) in enumerate(

        ranking,
        start=1

    ):

        metrics = results[
            model_name
        ]["metrics"]

        print(

            f"{rank:<5} "
            f"{model_name:<15} "
            f"{metrics['accuracy']:<8.3f} "
            f"{metrics['semantic']:<8.3f} "
            f"{metrics.get('factuality',0):<8.3f} "
            f"{metrics['reliability']:<8.3f} "
            f"{metrics['safety']:<8.3f} "
            f"{metrics['consistency']:<8.3f} "
            f"{metrics['variance']:<8.3f} "
            f"{metrics['hallucination']:<8.3f} "
            f"{metrics['latency(ms)']:<12.2f} "
            f"{drs_score:<8.3f}"

        )

    # =====================================================
    # RECOMMENDATION ENGINE
    # =====================================================

    engine = RecommendationEngine(
        results
    )

    recommendation = engine.recommend(
        use_case=dataset
    )

    # =====================================================
    # AI ADVISOR REPORT
    # =====================================================

    typer.echo(
        "\n=== AI ADVISOR REPORT ===\n"
    )

    typer.echo(

        f"✅ Recommended Model : "
        f"{recommendation.get('recommended_model', 'Unknown')}"

    )

    typer.echo(

        f"📊 Score             : "
        f"{recommendation.get('score', 0)}"

    )

    typer.echo(

        f"🧠 DRS               : "
        f"{recommendation.get('drs', 0)}"

    )

    typer.echo(

        f"🎯 Confidence        : "
        f"{recommendation.get('confidence', 0)}"

    )

    # =====================================================
    # HPI ANALYSIS
    # =====================================================

    recommended_model = recommendation.get(
        "recommended_model",
        "Unknown"
    )

    hallucination_score = results[
        recommended_model
    ]["metrics"].get(
        "hallucination",
        0
    )

    factuality_score = results[
        recommended_model
    ]["metrics"].get(
        "factuality",
        0
    )

    typer.echo(

        f"🧪 Hallucination Risk: "
        f"{hallucination_score:.3f}"

    )
    typer.echo(
        f"📚 Factuality Score  : "
        f"{factuality_score:.3f}"
    )

    if hallucination_score <= 0.20:

        typer.echo(
            "🟢 Low hallucination risk"
        )

    elif hallucination_score <= 0.40:

        typer.echo(
            "🟡 Moderate hallucination risk"
        )

    else:

        typer.echo(
            "🔴 High hallucination risk"
        )

    typer.echo("\n=== TRUST SUMMARY ===\n")
    drs = recommendation["drs"]
    if drs >= 0.85:
        typer.echo("🟢 Production Ready")
    elif drs >= 0.60:
        typer.echo("🟡 Caution Advised with Enterprise Capable")
    elif drs >= 0.35:
        typer.echo("🔴 Not Recommended Further Validation Recommended")
    else:
        typer.echo("⚠️ Critical Risk - Not Recommended")

    # =====================================================
    # WHY
    # =====================================================

    typer.echo("\nWhy:")

    typer.echo(

        f"→ {recommendation.get('reason', 'N/A')}"

    )

    # =====================================================
    # TRADEOFFS
    # =====================================================

    typer.echo("\nTrade-offs:")

    typer.echo(

        f"→ {recommendation['tradeoffs']}"

    )

    # =====================================================
    # RISKS
    # =====================================================

    typer.echo("\nRisks:")

    for risk in recommendation["risks"]:

        typer.echo(f"→ {risk}")

    # =====================================================
    # INSIGHTS
    # =====================================================

    if recommendation.get("insights"):

        typer.echo("\nInsights:")

        for insight in recommendation[
            "insights"
        ]:

            typer.echo(
                f"→ {insight}"
            )

    # =====================================================
    # GENERATE HTML REPORT
    # =====================================================

    if report:

        typer.echo(
            "\n📄 OpenVals AI Trust Assessment"
            "Evaluate • Benchmark • Trust Intelligence\n"
        )

        generate_html_report(
            results=results,
            recommendation=recommendation,
            output_file=str(output_path)
        )

        typer.echo(
            "\n✅ OpenVals AI Trust Assessment Complete:"
        )

        typer.echo(
            f"📁 {output_path.resolve()}"
        )

        typer.echo(
            "\n📊 Charts saved under:"
        )

        typer.echo(
            "📁 outputs/charts/"
        )

# =========================================================
# DATASETS
# =========================================================

@app.command("datasets")
def datasets():

    """
    List available datasets.
    """

    typer.echo(

        "\n📦 Available "
        "OpenVals Datasets\n"

    )

    print(

        f"{'Dataset':<15} "
        f"{'Domain':<15} "
        f"{'Description'}"

    )

    print("-" * 70)

    for name, info in DATASETS.items():

        print(

            f"{name:<15} "
            f"{info['domain']:<15} "
            f"{info['description']}"

        )

# =========================================================
# ENTRYPOINT
# =========================================================

def main():
    app()

if __name__ == "__main__":
    main()
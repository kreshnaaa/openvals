from openvals.explainability.insights import generate_insights
from openvals.explainability.narratives import executive_narrative
from openvals.explainability.anomalies import detect_anomalies


def explain_model(model_name, result):

    metrics = result["metrics"]

    drs = result.get("drs_score", 0)

    insights = generate_insights(metrics)

    narrative = executive_narrative(
        model_name,
        metrics,
        drs
    )

    anomalies = detect_anomalies(metrics)

    return {
        "narrative": narrative,
        "insights": insights,
        "anomalies": anomalies
    }
from datetime import datetime
import os

from openvals.reporting.charts import generate_all_charts
from openvals.reporting.report_styles import get_report_styles


# =========================================================
# TRUST CLASSIFICATION
# =========================================================

def classify_trust(drs):

    if drs >= 0.90:
        return "🟢 Production Ready"

    elif drs >= 0.75:
        return "🟡 Enterprise Capable"

    elif drs >= 0.50:
        return "🟠 Experimental"

    else:
        return "🔴 Unsafe / Unstable"


# =========================================================
# METRIC STATUS
# =========================================================

def metric_status(value, high=0.8, medium=0.6):

    if value >= high:
        return "🟢"

    elif value >= medium:
        return "🟡"

    return "🔴"


# =========================================================
# HALLUCINATION STATUS
# LOWER IS BETTER
# =========================================================

def hallucination_status(value):

    if value <= 0.20:
        return "🟢"

    elif value <= 0.50:
        return "🟡"

    return "🔴"


# =========================================================
# GENERATE HTML REPORT
# =========================================================

def generate_html_report(
    results,
    recommendation,
    output_file="report.html",
    charts_dir="charts"
):

    if recommendation is None:
        recommendation = {}

    deployment = recommendation.get("deployment") or {}

    deployment.setdefault("readiness", "Unknown")
    deployment.setdefault("recommendations", [])
    deployment.setdefault("risks", [])

    output_dir = os.path.dirname(
        os.path.abspath(output_file)
    )

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    charts_path = os.path.join(
        output_dir,
        charts_dir
    )

    os.makedirs(charts_path, exist_ok=True)

    generate_all_charts(
        results,
        charts_path
    )

    radar_chart = f"{charts_dir}/radar_chart.png"
    latency_chart = f"{charts_dir}/latency_chart.png"
    drs_chart = f"{charts_dir}/drs_chart.png"
    hallucination_chart = f"{charts_dir}/hallucination_chart.png"

    ranked = sorted(
        results.items(),
        key=lambda x: x[1].get("drs_score", 0),
        reverse=True
    )

    recommended_model = recommendation.get(
        "recommended_model",
        ""
    )

    recommended_metrics = {}

    if recommended_model in results:
        recommended_metrics = results[
            recommended_model
        ].get(
            "metrics",
            {}
        )

    recommended_factuality = recommended_metrics.get(
        "factuality",
        0
    )

    rows = ""

    for i, (model, data) in enumerate(ranked, 1):

        m = data.get("metrics", {})

        hallucination = m.get(
            "hallucination",
            0
        )

        rows += f"""
        <tr>
            <td>{i}</td>

            <td>
                <b>{model}</b>
            </td>

            <td>
                {metric_status(m.get('accuracy', 0))}
                {m.get('accuracy', 0):.3f}
            </td>

            <td>
                {metric_status(m.get('semantic', 0))}
                {m.get('semantic', 0):.3f}
            </td>

            <td>
                {metric_status(m.get('factuality', 0))}
                {m.get('factuality', 0):.3f}
            </td>

            <td>
                {metric_status(m.get('reliability', 0))}
                {m.get('reliability', 0):.3f}
            </td>

            <td>
                {metric_status(m.get('safety', 0))}
                {m.get('safety', 0):.3f}
            </td>

            <td>
                {metric_status(m.get('consistency', 0))}
                {m.get('consistency', 0):.3f}
            </td>

            <td>
                {metric_status(1 - m.get('variance', 0))}
                {m.get('variance', 0):.3f}
            </td>

            <td>
                {hallucination_status(hallucination)}
                {hallucination:.3f}
            </td>

            <td>
                {m.get('latency', 0):.2f}
            </td>

            <td>
                <b>{data.get('drs_score', 0):.3f}</b>
            </td>
        </tr>
        """

    risks_html = "".join(
        [
            f"<li>{r}</li>"
            for r in recommendation.get(
                "risks",
                []
            )
        ]
    )

    insights_html = "".join(
        [
            f"<li>{i}</li>"
            for i in recommendation.get(
                "insights",
                []
            )
        ]
    )

    if recommended_model in results:

        insights_html += (
            f"<li>Factuality Score for "
            f"{recommended_model}: "
            f"<b>{recommended_factuality:.3f}</b></li>"
        )

    tradeoffs_detail_html = "".join(
        [
            f"<li>{t}</li>"
            for t in recommendation.get(
                "tradeoffs_detail",
                []
            )
        ]
    )

    anomalies_html = "".join(
        [
            f"<li>{a}</li>"
            for a in recommendation.get(
                "anomalies",
                []
            )
        ]
    )

    deployment_html = "".join(
        [
            f"<li>{d}</li>"
            for d in deployment.get(
                "recommendations",
                []
            )
        ]
    )

    trust = classify_trust(
        recommendation.get("drs", 0)
    )

    summary = recommendation.get(
        "summary",
        f"""
        OpenVals recommends
        <b>{recommendation.get('recommended_model', 'Unknown')}</b>
        based on overall trustworthiness,
        factual accuracy, semantic quality,
        operational reliability,
        hallucination probability,
        and deployment confidence.
        """
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    html = f"""
    <html>
    <head>
        <title>OpenVals AI Evaluation Report</title>

        <style>
            {get_report_styles()}
        </style>
    </head>

    <body>
        <h1>OpenVals AI Evaluation Report</h1>

        <div class="subtitle">
            Generated on {timestamp}
        </div>

        <div class="card success">
            <h2>Executive Summary</h2>
            <p>{summary}</p>

            <div class="trust">
                Trust Classification: {trust}
            </div>
        </div>

        <div class="card">
            <h2>AI Advisor Recommendation</h2>

            <p>
                <b>Recommended Model:</b>
                <span class="highlight">
                    {recommendation.get('recommended_model', 'Unknown')}
                </span>
            </p>

            <div class="metric-box">
                <b>Score</b><br>
                {recommendation.get('score', 0)}
            </div>

            <div class="metric-box">
                <b>DRS</b><br>
                {recommendation.get('drs', 0)}
            </div>

            <div class="metric-box">
                <b>Confidence</b><br>
                {recommendation.get('confidence', 0)}
            </div>

            <div class="metric-box">
                <b>Factuality</b><br>
                {recommended_factuality:.3f}
            </div>

            <hr>

            <p>
                <b>Why Recommended:</b><br>
                {recommendation.get('reason', 'No reason provided')}
            </p>

            <p>
                <b>Trade-offs:</b><br>
                {recommendation.get('tradeoffs', 'None')}
            </p>
        </div>

        <div class="card">
            <h2>Visual Intelligence Dashboard</h2>

            <h3>Radar Analysis</h3>
            <img src="{radar_chart}" class="chart" alt="Radar Chart">

            <hr>

            <h3>Latency Comparison</h3>
            <img src="{latency_chart}" class="chart" alt="Latency Chart">

            <hr>

            <h3>DRS Comparison</h3>
            <img src="{drs_chart}" class="chart" alt="DRS Chart">

            <hr>

            <h3>Hallucination Risk Comparison</h3>
            <img
                src="{hallucination_chart}"
                class="chart"
                alt="Hallucination Chart"
            >
        </div>

        <div class="card">
            <h2>Deployment Readiness</h2>

            <div class="deployment">
                {deployment.get("readiness", "Unknown")}
            </div>

            <ul>
                {deployment_html}
            </ul>
        </div>

        <div class="card info">
            <h2>Operational Insights</h2>

            <ul>
                {insights_html}
            </ul>
        </div>

        <div class="card">
            <h2>Tradeoff Analysis</h2>

            <ul>
                {tradeoffs_detail_html}
            </ul>
        </div>

        <div class="card warning">
            <h2>Risk Analysis</h2>

            <ul>
                {risks_html}
            </ul>
        </div>

        <div class="card warning">
            <h2>Detected Anomalies</h2>

            <ul>
                {anomalies_html}
            </ul>
        </div>

        <div class="card">
            <h2>Model Leaderboard</h2>

            <table>
                <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>Semantic</th>
                    <th>Factuality</th>
                    <th>Reliability</th>
                    <th>Safety</th>
                    <th>Consistency</th>
                    <th>Variance</th>
                    <th>Hallucination</th>
                    <th>Latency(ms)</th>
                    <th>DRS</th>
                </tr>

                {rows}
            </table>
        </div>

        <div class="footer">
            Built with OpenVals •
            AI Trust & Validation Framework

            <br><br>

            Developed by DrPinnacle
        </div>
    </body>
    </html>
    """

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print(
        f"✅ HTML report generated: {output_file}"
    )
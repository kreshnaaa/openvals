from datetime import datetime
import os

from openvals.reporting.charts import generate_all_charts
from openvals.reporting.report_styles import get_report_styles

from openvals.reporting.report_sections import (
    build_hero_section,
    build_executive_summary,
    build_executive_metric_cards,
    build_ai_advisor_section,
    build_trust_intelligence_dashboard,
    build_visual_dashboard,
    build_deployment_section,
    build_insights_section,
    build_tradeoffs_section,
    build_risk_section,
    build_leaderboard_section,
    build_governance_section,
    build_footer
)


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
# LIST BUILDER
# =========================================================

def build_list_html(items):

    return "".join(
        [
            f"<li>{item}</li>"
            for item in items
        ]
    )


# =========================================================
# GENERATE HTML REPORT
# =========================================================

def generate_html_report(
    results,
    recommendation,
    output_file="report.html",
    charts_dir="charts",
    dataset_name="OpenVals Benchmark",
    config_name="Default"
):

    if recommendation is None:
        recommendation = {}

    deployment = recommendation.get("deployment") or {}

    deployment.setdefault(
        "readiness",
        "Unknown"
    )

    deployment.setdefault(
        "recommendations",
        []
    )

    deployment.setdefault(
        "risks",
        []
    )

    # =====================================================
    # DIRECTORIES
    # =====================================================

    output_dir = os.path.dirname(
        os.path.abspath(output_file)
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    charts_path = os.path.join(
        output_dir,
        charts_dir
    )

    os.makedirs(
        charts_path,
        exist_ok=True
    )

    # =====================================================
    # CHARTS
    # =====================================================

    generate_all_charts(
        results,
        charts_path
    )

    radar_chart = f"{charts_dir}/radar_chart.png"
    latency_chart = f"{charts_dir}/latency_chart.png"
    drs_chart = f"{charts_dir}/drs_chart.png"
    hallucination_chart = f"{charts_dir}/hallucination_chart.png"

    # =====================================================
    # RANKING
    # =====================================================

    ranked = sorted(
        results.items(),
        key=lambda x: x[1].get(
            "drs_score",
            0
        ),
        reverse=True
    )

    # =====================================================
    # RECOMMENDED MODEL METRICS
    # =====================================================

    recommended_model = recommendation.get(
        "recommended_model",
        "Unknown"
    )

    recommended_metrics = results.get(
        recommended_model,
        {}
    ).get(
        "metrics",
        {}
    )

    recommended_factuality = recommended_metrics.get(
        "factuality",
        0
    )

    performance_score = (
        recommended_metrics.get("accuracy", 0)
        +
        recommended_metrics.get("semantic", 0)
    ) / 2

    trust_score = (
        recommended_metrics.get("reliability", 0)
        +
        recommended_metrics.get("safety", 0)
        +
        recommended_metrics.get("factuality", 0)
    ) / 3

    # =====================================================
    # TABLE ROWS
    # =====================================================

    rows = ""

    for i, (model, data) in enumerate(
        ranked,
        1
    ):

        m = data.get(
            "metrics",
            {}
        )

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

    # =====================================================
    # HTML CONTENT BLOCKS
    # =====================================================

    risks_html = build_list_html(
        recommendation.get(
            "risks",
            []
        )
    )

    insights_html = build_list_html(
        recommendation.get(
            "insights",
            []
        )
    )

    if recommended_model in results:

        insights_html += (
            f"<li>Factuality Score for "
            f"{recommended_model}: "
            f"<b>{recommended_factuality:.3f}</b></li>"
        )

    tradeoffs_detail_html = build_list_html(
        recommendation.get(
            "tradeoffs_detail",
            []
        )
    )

    anomalies_html = build_list_html(
        recommendation.get(
            "anomalies",
            []
        )
    )

    deployment_html = build_list_html(
        deployment.get(
            "recommendations",
            []
        )
    )

    trust = classify_trust(
        recommendation.get(
            "drs",
            0
        )
    )

    summary = recommendation.get(
        "summary",
        f"""
        OpenVals recommends
        <b>{recommendation.get('recommended_model', 'Unknown')}</b>
        based on overall trustworthiness, factual accuracy,
        semantic quality, operational reliability,
        hallucination probability, and deployment confidence.
        """
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    trust_dashboard_metrics = {
        **recommended_metrics,
        "drs": recommendation.get(
            "drs",
            0
        )
    }

    # =====================================================
    # HTML TEMPLATE
    # =====================================================

    html = f"""
    <html>

    <head>
        <title>
            OpenVals AI Trust Intelligence Report
        </title>

        {get_report_styles()}
    </head>

    <body>

        <div class="report-shell">

            {build_hero_section(
                recommendation,
                trust,
                timestamp,
                dataset_name=dataset_name,
                model_count=len(results),
                config_name=config_name
            )}

            {build_executive_metric_cards(
                performance_score,
                trust_score
            )}

            {build_executive_summary(
                summary,
                trust
            )}

            {build_ai_advisor_section(
                recommendation,
                recommended_factuality
            )}

            {build_trust_intelligence_dashboard(
                trust_dashboard_metrics
            )}

            {build_visual_dashboard(
                radar_chart,
                latency_chart,
                drs_chart,
                hallucination_chart
            )}

            {build_deployment_section(
                deployment.get(
                    "readiness",
                    "Unknown"
                ),
                deployment_html
            )}

            {build_insights_section(
                insights_html
            )}

            {build_tradeoffs_section(
                tradeoffs_detail_html
            )}

            {build_risk_section(
                risks_html,
                anomalies_html
            )}

            {build_leaderboard_section(
                rows
            )}

            {build_governance_section()}

            {build_footer()}

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
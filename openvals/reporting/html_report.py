from datetime import datetime


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
# GENERATE HTML REPORT
# =========================================================

def generate_html_report(
    results,
    recommendation,
    output_file="report.html"
):

    # =====================================================
    # SAFE DEFAULTS
    # =====================================================

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
    # SORT MODELS
    # =====================================================

    ranked = sorted(
        results.items(),
        key=lambda x: x[1].get("drs_score", 0),
        reverse=True
    )

    # =====================================================
    # BUILD TABLE ROWS
    # =====================================================

    rows = ""

    for i, (model, data) in enumerate(ranked, 1):

        m = data.get("metrics", {})

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
                {m.get('latency', 0):.2f}
            </td>

            <td>
                <b>{data.get('drs_score', 0):.3f}</b>
            </td>

        </tr>
        """

    # =====================================================
    # RISKS
    # =====================================================

    risks_html = "".join(
        [
            f"<li>{r}</li>"
            for r in recommendation.get(
                "risks",
                []
            )
        ]
    )

    # =====================================================
    # INSIGHTS
    # =====================================================

    insights_html = "".join(
        [
            f"<li>{i}</li>"
            for i in recommendation.get(
                "insights",
                []
            )
        ]
    )

    # =====================================================
    # TRADEOFF DETAILS
    # =====================================================

    tradeoffs_detail_html = "".join(
        [
            f"<li>{t}</li>"
            for t in recommendation.get(
                "tradeoffs_detail",
                []
            )
        ]
    )

    # =====================================================
    # ANOMALIES
    # =====================================================

    anomalies_html = "".join(
        [
            f"<li>{a}</li>"
            for a in recommendation.get(
                "anomalies",
                []
            )
        ]
    )

    # =====================================================
    # DEPLOYMENT DETAILS
    # =====================================================

    deployment_html = "".join(
        [
            f"<li>{d}</li>"
            for d in deployment.get(
                "recommendations",
                []
            )
        ]
    )

    # =====================================================
    # TRUST CLASSIFICATION
    # =====================================================

    trust = classify_trust(
        recommendation.get("drs", 0)
    )

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    summary = recommendation.get(
        "summary",
        f"""
        OpenVals recommends
        <b>{recommendation.get('recommended_model', 'Unknown')}</b>
        based on DRS performance,
        semantic capability,
        operational reliability,
        and deployment confidence.
        """
    )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # HTML TEMPLATE
    # =====================================================

    html = f"""
    <html>

    <head>

        <title>OpenVals AI Evaluation Report</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 30px;
                color: #222;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            h2 {{
                margin-top: 0;
                color: #111827;
            }}

            h3 {{
                margin-top: 20px;
                color: #1f2937;
            }}

            .subtitle {{
                color: #666;
                margin-bottom: 30px;
            }}

            .card {{
                background: white;
                padding: 24px;
                margin-bottom: 25px;
                border-radius: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-left: 6px solid #4f46e5;
            }}

            .warning {{
                border-left: 6px solid #ef4444;
            }}

            .success {{
                border-left: 6px solid #16a34a;
            }}

            .info {{
                border-left: 6px solid #0284c7;
            }}

            .highlight {{
                color: #0b7a32;
                font-weight: bold;
            }}

            .trust {{
                font-size: 20px;
                font-weight: bold;
                margin-top: 10px;
            }}

            .deployment {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #2563eb;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            th {{
                background: #111827;
                color: white;
                padding: 14px;
                text-align: center;
            }}

            td {{
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
                text-align: center;
                background: white;
            }}

            tr:hover td {{
                background: #f9fafb;
            }}

            ul {{
                margin-top: 8px;
                line-height: 1.7;
            }}

            .metric-box {{
                display: inline-block;
                margin-right: 20px;
                margin-top: 10px;
                padding: 14px;
                min-width: 120px;
                background: #f9fafb;
                border-radius: 10px;
                text-align: center;
            }}

            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #777;
                font-size: 14px;
            }}

            hr {{
                border: none;
                border-top: 1px solid #e5e7eb;
                margin: 20px 0;
            }}

        </style>

    </head>

    <body>

        <h1>OpenVals AI Evaluation Report</h1>

        <div class="subtitle">
            Generated on {timestamp}
        </div>

        <!-- EXECUTIVE SUMMARY -->

        <div class="card success">

            <h2>Executive Summary</h2>

            <p>{summary}</p>

            <div class="trust">
                Trust Classification: {trust}
            </div>

        </div>

        <!-- RECOMMENDATION -->

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

        <!-- DEPLOYMENT READINESS -->

        <div class="card">

            <h2>Deployment Readiness Intelligence</h2>

            <div class="deployment">
                {deployment.get("readiness", "Unknown")}
            </div>

            <ul>
                {deployment_html}
            </ul>

        </div>

        <!-- INSIGHTS -->

        <div class="card info">

            <h2>Operational Insights</h2>

            <ul>
                {insights_html}
            </ul>

        </div>

        <!-- TRADEOFF DETAILS -->

        <div class="card">

            <h2>⚖️ Tradeoff Analysis</h2>

            <ul>
                {tradeoffs_detail_html}
            </ul>

        </div>

        <!-- RISKS -->

        <div class="card warning">

            <h2>Risk Analysis</h2>

            <ul>
                {risks_html}
            </ul>

        </div>

        <!-- ANOMALIES -->

        <div class="card warning">

            <h2>Detected Anomalies</h2>

            <ul>
                {anomalies_html}
            </ul>

        </div>

        <!-- LEADERBOARD -->

        <div class="card">

            <h2>Model Leaderboard</h2>

            <table>

                <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>Semantic</th>
                    <th>Reliability</th>
                    <th>Safety</th>
                    <th>Consistency</th>
                    <th>Variance</th>
                    <th>Latency(ms)</th>
                    <th>DRS</th>
                </tr>

                {rows}

            </table>

        </div>

        <!-- FOOTER -->

        <div class="footer">

            Built with OpenVals • AI Trust & Validation Framework<br><br>

            Developed by DrPinnacle

        </div>

    </body>

    </html>
    """

    # =====================================================
    # SAVE FILE
    # =====================================================

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML report generated: {output_file}")
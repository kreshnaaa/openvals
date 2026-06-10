# =========================================================
# SAFE FORMATTERS
# =========================================================

def fmt_score(value, digits=3):

    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "0.000"


def fmt_percent(value):

    try:
        return f"{float(value) * 100:.1f}%"
    except Exception:
        return "0.0%"


def safe_get(data, key, default=0):

    if not isinstance(data, dict):
        return default

    return data.get(key, default)


# =========================================================
# HERO SECTION
# =========================================================

def build_hero_section(
    recommendation,
    trust,
    timestamp,
    dataset_name="Unknown",
    model_count=0,
    config_name="default",
    logo_path="assets/logo.png"
):

    recommended_model = recommendation.get(
        "recommended_model",
        "Unknown"
    )

    drs = recommendation.get(
        "drs",
        0
    )

    confidence = recommendation.get(
        "confidence",
        0
    )

    return f"""
    <div class="hero">

        <div class="hero-top">

            <div>

                <div class="brand-row">

                    <img
                        src="{logo_path}"
                        class="brand-logo"
                        alt="OpenVals Logo"
                    >

                    <div class="brand-name">
                        OpenVals
                    </div>

                </div>

                <h1>
                    AI Trust Intelligence Report
                </h1>

                <div class="hero-subtitle">
                    Comprehensive evaluation of AI models across
                    trust, performance, factuality, hallucination,
                    and operational readiness.
                </div>

                <div class="meta-row">

                    <div class="pill">
                        Dataset: {dataset_name}
                    </div>

                    <div class="pill">
                        Models Evaluated: {model_count}
                    </div>

                    <div class="pill">
                        Configuration: {config_name}
                    </div>

                    <div class="pill">
                        Generated: {timestamp}
                    </div>

                </div>

            </div>

            <div class="hero-score">

                <div class="hero-score-label">
                    Recommended Model
                </div>

                <div class="hero-score-caption">
                    {recommended_model}
                </div>

                <hr>

                <div class="hero-score-label">
                    DRS Score
                </div>

                <div class="hero-score-value">
                    {fmt_score(drs)}
                </div>

                <div class="hero-score-caption">
                    {trust}
                </div>

                <div class="hero-score-caption">
                    Confidence: {confidence}
                </div>

            </div>

        </div>

    </div>
    """


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

def build_executive_summary(
    summary,
    trust
):

    return f"""
    <div class="card success">

        <div class="section-label">
            Executive Overview
        </div>

        <h2>
            Executive Summary
        </h2>

        <p>
            {summary}
        </p>

        <div class="trust">
            Trust Classification: {trust}
        </div>

    </div>
    """


# =========================================================
# EXECUTIVE METRIC CARDS
# =========================================================

def build_metric_card(
    label,
    value,
    note="",
    status=""
):

    return f"""
    <div class="metric-card">

        <div class="metric-label">
            {label}
        </div>

        <div class="metric-value">
            {value}
        </div>

        <div class="metric-note">
            {status} {note}
        </div>

    </div>
    """


def build_executive_metric_cards(
    performance_score,
    trust_score,
    infrastructure_score="N/A",
    governance_score="N/A"
):

    return f"""
    <div class="grid grid-4">

        {build_metric_card(
            "Performance",
            fmt_score(performance_score),
            "Model capability and response quality"
        )}

        {build_metric_card(
            "Trust Intelligence",
            fmt_score(trust_score),
            "Reliability, factuality, safety, and HPI"
        )}

        {build_metric_card(
            "Infrastructure",
            infrastructure_score,
            "Compute, energy, and carbon metrics"
        )}

        {build_metric_card(
            "Governance",
            governance_score,
            "Compliance and policy readiness"
        )}

    </div>
    """


# =========================================================
# AI ADVISOR SECTION
# =========================================================

def build_ai_advisor_section(
    recommendation,
    recommended_factuality=0
):

    return f"""
    <div class="card">

        <div class="section-label">
            Recommendation Engine
        </div>

        <h2>
            AI Advisor Recommendation
        </h2>

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
            {fmt_score(recommended_factuality)}
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
    """


# =========================================================
# TRUST INTELLIGENCE DASHBOARD
# =========================================================

def build_trust_intelligence_dashboard(
    metrics
):

    drs = metrics.get(
        "drs",
        metrics.get("drs_score", 0)
    )

    factuality = metrics.get("factuality", 0)
    reliability = metrics.get("reliability", 0)
    safety = metrics.get("safety", 0)
    consistency = metrics.get("consistency", 0)
    hallucination = metrics.get("hallucination", 0)
    variance = metrics.get("variance", 0)

    return f"""
    <div class="card">

        <div class="section-label">
            Trust Intelligence
        </div>

        <h2>
            Trust Intelligence Dashboard
        </h2>

        <div class="grid grid-4">

            {build_metric_card(
                "DRS",
                fmt_score(drs),
                "Decision Reliability Score"
            )}

            {build_metric_card(
                "Factuality",
                fmt_score(factuality),
                "Truth alignment against expected output"
            )}

            {build_metric_card(
                "Safety",
                fmt_score(safety),
                "Unsafe behavior resistance"
            )}

            {build_metric_card(
                "Reliability",
                fmt_score(reliability),
                "Stability across evaluations"
            )}

            {build_metric_card(
                "Consistency",
                fmt_score(consistency),
                "Repeatability of responses"
            )}

            {build_metric_card(
                "Hallucination",
                fmt_score(hallucination),
                "Lower is better"
            )}

            {build_metric_card(
                "Variance",
                fmt_score(variance),
                "Lower is better"
            )}

        </div>

    </div>
    """


# =========================================================
# VISUAL DASHBOARD
# =========================================================

def build_visual_dashboard(
    radar_chart,
    latency_chart,
    drs_chart,
    hallucination_chart
):

    return f"""
    <div class="card">

        <div class="section-label">
            Visual Analytics
        </div>

        <h2>
            Visual Intelligence Dashboard
        </h2>

        <div class="grid grid-2">

            <div>
                <h3>Radar Analysis</h3>
                <img
                    src="{radar_chart}"
                    class="chart"
                    alt="Radar Chart"
                >
            </div>

            <div>
                <h3>DRS Comparison</h3>
                <img
                    src="{drs_chart}"
                    class="chart"
                    alt="DRS Chart"
                >
            </div>

            <div>
                <h3>Latency Comparison</h3>
                <img
                    src="{latency_chart}"
                    class="chart"
                    alt="Latency Chart"
                >
            </div>

            <div>
                <h3>Hallucination Risk</h3>
                <img
                    src="{hallucination_chart}"
                    class="chart"
                    alt="Hallucination Chart"
                >
            </div>

        </div>

    </div>
    """


# =========================================================
# DEPLOYMENT READINESS
# =========================================================

def build_deployment_section(
    readiness,
    deployment_html
):

    return f"""
    <div class="card">

        <div class="section-label">
            Deployment
        </div>

        <h2>
            Deployment Readiness
        </h2>

        <div class="deployment">
            {readiness}
        </div>

        <ul>
            {deployment_html}
        </ul>

    </div>
    """


# =========================================================
# OPERATIONAL INSIGHTS
# =========================================================

def build_insights_section(
    insights_html
):

    return f"""
    <div class="card info">

        <div class="section-label">
            Intelligence
        </div>

        <h2>
            Operational Insights
        </h2>

        <ul>
            {insights_html}
        </ul>

    </div>
    """


# =========================================================
# TRADEOFFS
# =========================================================

def build_tradeoffs_section(
    tradeoffs_detail_html
):

    return f"""
    <div class="card">

        <div class="section-label">
            Decision Context
        </div>

        <h2>
            Tradeoff Analysis
        </h2>

        <ul>
            {tradeoffs_detail_html}
        </ul>

    </div>
    """


# =========================================================
# RISK SECTION
# =========================================================

def build_risk_section(
    risks_html,
    anomalies_html
):

    return f"""
    <div class="grid grid-2">

        <div class="card warning">

            <div class="section-label">
                Risk Intelligence
            </div>

            <h2>
                Risk Analysis
            </h2>

            <ul>
                {risks_html}
            </ul>

        </div>

        <div class="card warning">

            <div class="section-label">
                Detection
            </div>

            <h2>
                Detected Anomalies
            </h2>

            <ul>
                {anomalies_html}
            </ul>

        </div>

    </div>
    """


# =========================================================
# LEADERBOARD
# =========================================================

def build_leaderboard_section(
    rows
):

    return f"""
    <div class="card">

        <div class="section-label">
            Model Comparison
        </div>

        <h2>
            Model Leaderboard
        </h2>

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
    """


# =========================================================
# GOVERNANCE PLACEHOLDER
# =========================================================

def build_governance_section():

    return """
    <div class="card">

        <div class="section-label">
            Governance
        </div>

        <h2>
            Governance Intelligence
        </h2>

        <p>
            Governance, auditability, compliance mapping,
            policy alignment, and enterprise risk controls
            will be available in upcoming OpenVals releases.
        </p>

        <div class="grid grid-3">

            <div class="metric-card">
                <div class="metric-label">Compliance</div>
                <div class="metric-value">N/A</div>
                <div class="metric-note">Coming soon</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Auditability</div>
                <div class="metric-value">N/A</div>
                <div class="metric-note">Coming soon</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Policy Risk</div>
                <div class="metric-value">N/A</div>
                <div class="metric-note">Coming soon</div>
            </div>

        </div>

    </div>
    """


# =========================================================
# FOOTER
# =========================================================

def build_footer():

    return """
    <div class="footer">

        Built with OpenVals •
        AI Trust & Validation Framework

        <br><br>

        Developed by DrPinnacle

    </div>
    """
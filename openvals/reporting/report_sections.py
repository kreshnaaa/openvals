def build_hero_section(
    recommendation,
    trust,
    timestamp
):

    return f"""
    <div class="hero">

        <div class="hero-top">

            <div>

                <div class="brand-row">

                    <img
                        src="assets/logo.png"
                        class="brand-logo"
                    >

                    <div class="brand-name">
                        OpenVals
                    </div>

                </div>

                <h1>
                    AI Trust Intelligence Report
                </h1>

                <div class="hero-subtitle">

                    Evaluate.
                    Benchmark.
                    Trust Intelligence.

                </div>

            </div>

            <div class="hero-score">

                <div class="hero-score-label">
                    DRS Score
                </div>

                <div class="hero-score-value">
                    {recommendation.get("drs", 0)}
                </div>

                <div class="hero-score-caption">
                    {trust}
                </div>

            </div>

        </div>

        <div class="meta-row">

            <div class="pill">
                Recommended:
                {recommendation.get(
                    "recommended_model",
                    "Unknown"
                )}
            </div>

            <div class="pill">
                Confidence:
                {recommendation.get(
                    "confidence",
                    0
                )}
            </div>

            <div class="pill">
                Generated:
                {timestamp}
            </div>

        </div>

    </div>
    """
HALLUCINATION_PATTERNS = [

    "definitely",
    "guaranteed",
    "always",
    "never",
    "100%",
    "confirmed",
    "proven",
    "undoubtedly",
    "no risk",
    "cannot fail",
    "certainly",
    "everyone knows",
    "scientifically proven"

]


def detect_overconfidence(text):

    text = text.lower()

    matches = []

    for pattern in HALLUCINATION_PATTERNS:

        if pattern in text:

            matches.append(pattern)

    return {

        "score": min(
            len(matches) * 0.1,
            1.0
        ),

        "matches": matches

    }


def compute_hpi(

    semantic_score,
    consistency_score,
    variance_score,
    overconfidence_score

):

    semantic_risk = (
        1 - semantic_score
    )

    consistency_risk = (
        1 - consistency_score
    )

    variance_risk = variance_score

    overconfidence_risk = (
        overconfidence_score
    )

    hpi = (

        semantic_risk * 0.35 +

        consistency_risk * 0.25 +

        variance_risk * 0.25 +

        overconfidence_risk * 0.15

    )

    return round(
        min(max(hpi, 0), 1),
        4
    )


def hallucination_analysis(

    output_text,
    metrics

):

    overconfidence = detect_overconfidence(
        output_text
    )

    hpi = compute_hpi(

        semantic_score=metrics.get(
            "semantic",
            0
        ),

        consistency_score=metrics.get(
            "consistency",
            0
        ),

        variance_score=metrics.get(
            "variance",
            0
        ),

        overconfidence_score=overconfidence[
            "score"
        ]

    )

    # ==========================================
    # CLASSIFICATION
    # ==========================================

    if hpi < 0.25:

        risk = "Low"

    elif hpi < 0.50:

        risk = "Moderate"

    elif hpi < 0.75:

        risk = "High"

    else:

        risk = "Critical"

    return {

        "hpi_score": hpi,

        "risk_level": risk,

        "overconfidence_matches":
            overconfidence["matches"]

    }
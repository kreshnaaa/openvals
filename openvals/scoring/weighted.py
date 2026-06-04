# =========================================================
# WEIGHTED SCORING ENGINE
# =========================================================

def weighted_score(

    metrics,
    weights

):

    """
    Generic weighted scoring engine
    used for benchmarking and ranking.
    """

    # =====================================================
    # LATENCY NORMALIZATION
    # =====================================================

    latency = metrics.get(
        "latency",
        0
    )

    latency_score = 1 / (

        1 + latency / 1000

    )

    # =====================================================
    # NORMALIZED METRICS
    # =====================================================

    normalized = {

        "accuracy": metrics.get(
            "accuracy",
            0
        ),

        "semantic": metrics.get(
            "semantic",
            0
        ),

        "reliability": metrics.get(
            "reliability",
            0
        ),

        "safety": metrics.get(
            "safety",
            0
        ),

        "consistency": metrics.get(
            "consistency",
            0
        ),

        "variance": 1 - metrics.get(
            "variance",
            0
        ),

        "hallucination": 1 - metrics.get(
            "hallucination",
            0
        ),

        "factuality": metrics.get("factuality", 0),

        "latency": latency_score

    }

    # =====================================================
    # COMPUTE SCORE
    # =====================================================

    score = 0.0

    for metric, weight in weights.items():

        score += (

            normalized.get(metric, 0)

            * weight

        )

    return round(score, 4)
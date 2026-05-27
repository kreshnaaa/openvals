# =========================================================
# DECISION RELIABILITY SCORE (DRS)
# =========================================================

def compute_drs(

    metrics,
    weights=None

):

    """
    DRS evaluates whether a model
    is safe and reliable enough
    for production deployment.

    Higher is better.
    """

    # =====================================================
    # DEFAULT WEIGHTS
    # =====================================================

    weights = weights or {

        "accuracy": 0.25,
        "semantic": 0.15,
        "reliability": 0.20,
        "safety": 0.15,
        "consistency": 0.10,
        "variance": 0.05,
        "latency": 0.05,
        "hallucination": 0.05

    }

    # =====================================================
    # METRICS
    # =====================================================

    accuracy = metrics.get(
        "accuracy",
        0
    )

    semantic = metrics.get(
        "semantic",
        0
    )

    reliability = metrics.get(
        "reliability",
        0
    )

    safety = metrics.get(
        "safety",
        0
    )

    consistency = metrics.get(
        "consistency",
        0
    )

    variance = metrics.get(
        "variance",
        0
    )

    hallucination = metrics.get(
        "hallucination",
        0
    )

    latency = metrics.get(
        "latency",
        0
    )

    # =====================================================
    # LATENCY NORMALIZATION
    # =====================================================

    latency_score = 1 / (

        1 + (latency / 1000)

    )

    # =====================================================
    # DRS COMPUTATION
    # =====================================================

    drs = (

        weights["accuracy"] * accuracy +

        weights["semantic"] * semantic +

        weights["reliability"] * reliability +

        weights["safety"] * safety +

        weights["consistency"] * consistency +

        weights["latency"] * latency_score -

        weights["variance"] * variance -

        weights["hallucination"] * hallucination

    )

    # =====================================================
    # CLIP
    # =====================================================

    drs = max(

        0.0,
        min(1.0, drs)

    )

    return round(drs, 4)
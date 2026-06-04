# DECISION RELIABILITY SCORE (DRS)

def compute_drs(metrics, weights=None):

    """
    DRS evaluates whether a model is safe,
    factual, and reliable enough for production.

    Higher is better.
    """

    weights = weights or {
        "accuracy": 0.20,
        "semantic": 0.15,
        "factuality": 0.15,
        "reliability": 0.15,
        "safety": 0.15,
        "consistency": 0.10,
        "variance": 0.04,
        "latency": 0.03,
        "hallucination": 0.03
    }

    accuracy = metrics.get("accuracy", 0)
    semantic = metrics.get("semantic", 0)
    factuality = metrics.get("factuality", 0)
    reliability = metrics.get("reliability", 0)
    safety = metrics.get("safety", 0)
    consistency = metrics.get("consistency", 0)
    variance = metrics.get("variance", 0)
    hallucination = metrics.get("hallucination", 0)
    latency = metrics.get("latency", 0)

    latency_score = 1 / (1 + (latency / 1000))

    drs = (
        weights["accuracy"] * accuracy +
        weights["semantic"] * semantic +
        weights["factuality"] * factuality +
        weights["reliability"] * reliability +
        weights["safety"] * safety +
        weights["consistency"] * consistency +
        weights["latency"] * latency_score -
        weights["variance"] * variance -
        weights["hallucination"] * hallucination
    )

    drs = max(0.0, min(1.0, drs))

    return round(drs, 4)
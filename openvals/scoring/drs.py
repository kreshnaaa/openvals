def compute_drs(metrics, weights=None):
    weights = weights or {
        "accuracy": 0.3,
        "reliability": 0.25,
        "consistency": 0.25,
        "variance": 0.2
    }

    drs = (
        weights["accuracy"] * metrics.get("accuracy", 0) +
        weights["reliability"] * metrics.get("reliability", 0) +
        weights["consistency"] * metrics.get("consistency", 0) -
        weights["variance"] * metrics.get("variance", 0)
    )

    return max(0.0, min(1.0, drs))
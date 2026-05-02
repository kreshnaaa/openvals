
def weighted_score(metrics, weights):
    # normalize latency (lower is better)
    latency = metrics["latency"]

    # simple normalization (tunable)
    latency_score = 1 / (1 + latency / 1000)

    normalized = {
        "accuracy": metrics["accuracy"],
        "semantic": metrics["semantic"],
        "latency": latency_score
    }

    score = 0
    for k, w in weights.items():
        score += normalized.get(k, 0) * w

    return score

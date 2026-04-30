
def weighted_score(metrics: dict, weights: dict) -> float:
    return sum(metrics[k] * weights.get(k, 0) for k in metrics)

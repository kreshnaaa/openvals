
def rank_models(normalized_scores, weights):
    scores = {}
    for model, metrics in normalized_scores.items():
        total = sum(metrics[m] * weights.get(m, 0) for m in metrics)
        scores[model] = total
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

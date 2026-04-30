
def normalize_scores(results):
    normalized = {}
    metric_keys = results[list(results.keys())[0]]["metrics"].keys()

    for metric in metric_keys:
        values = [results[m]["metrics"][metric] for m in results]
        min_v, max_v = min(values), max(values)

        for model in results:
            val = results[model]["metrics"][metric]
            if max_v - min_v == 0:
                score = 1.0
            else:
                score = (val - min_v) / (max_v - min_v)

            normalized.setdefault(model, {})
            normalized[model][metric] = score

    return normalized

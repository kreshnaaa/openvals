def normalize_scores(results):
    metrics = ["accuracy", "semantic", "latency"]

    # collect values
    values = {m: [] for m in metrics}

    for model in results:
        for m in metrics:
            values[m].append(results[model]["metrics"][m])

    # min-max per metric
    min_vals = {m: min(values[m]) for m in metrics}
    max_vals = {m: max(values[m]) for m in metrics}

    normalized = {}

    for model in results:
        normalized[model] = {}

        for m in metrics:
            val = results[model]["metrics"][m]
            min_v = min_vals[m]
            max_v = max_vals[m]

            if max_v == min_v:
                norm = 1.0  # all equal
            else:
                if m == "latency":
                    # 🔥 INVERTED NORMALIZATION
                    norm = (max_v - val) / (max_v - min_v)
                else:
                    # normal case (higher is better)
                    norm = (val - min_v) / (max_v - min_v)

            normalized[model][m] = norm

    return normalized
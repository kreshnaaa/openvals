def generate_tradeoffs(metrics):

    tradeoffs = []

    latency = metrics.get("latency", 0)
    semantic = metrics.get("semantic", 0)
    consistency = metrics.get("consistency", 0)
    variance = metrics.get("variance", 0)

    if semantic >= 0.90 and latency > 5000:
        tradeoffs.append(
            "Higher semantic quality comes with increased latency."
        )

    if consistency < 0.70:
        tradeoffs.append(
            "Output consistency may fluctuate across runs."
        )

    if variance > 0.35:
        tradeoffs.append(
            "Elevated output variance may reduce predictability."
        )

    if latency <= 1500:
        tradeoffs.append(
            "Optimized for lower-latency workloads."
        )


    if not tradeoffs:
        tradeoffs.append(
            "Balanced tradeoff profile detected."
        )

    return tradeoffs
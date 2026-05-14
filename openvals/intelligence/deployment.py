def deployment_readiness(metrics):

    readiness = "Experimental"

    reasons = []

    if metrics["accuracy"] >= 0.85:
        reasons.append("Strong accuracy")

    if metrics["reliability"] >= 0.80:
        reasons.append("Reliable behavior")

    if metrics["consistency"] >= 0.80:
        reasons.append("Stable outputs")

    if metrics["safety"] < 0.70:
        reasons.append("Safety concerns detected")

    if metrics["latency"] > 8000:
        reasons.append("Latency too high for production")

    # FINAL CLASSIFICATION

    if (
        metrics["accuracy"] >= 0.85 and
        metrics["reliability"] >= 0.80 and
        metrics["consistency"] >= 0.80 and
        metrics["safety"] >= 0.85
    ):
        readiness = "Production Ready"

    elif metrics["accuracy"] >= 0.70:
        readiness = "Enterprise Capable"

    return {
        "readiness": readiness,
        "reasons": reasons
    }
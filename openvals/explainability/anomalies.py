def detect_anomalies(metrics):

    anomalies = []

    if metrics.get("accuracy", 1) > 0.9 and \
       metrics.get("semantic", 1) < 0.5:

        anomalies.append(
            "Possible overfitting or exact-match bias detected."
        )

    if metrics.get("latency", 0) > 15000:

        anomalies.append(
            "High latency anomaly detected."
        )

    if metrics.get("variance", 0) > 0.5:

        anomalies.append(
            "High output variability observed."
        )

    return anomalies
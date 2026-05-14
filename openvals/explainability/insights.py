def generate_insights(metrics):

    insights = []

    accuracy = metrics.get("accuracy", 0.0)
    semantic = metrics.get("semantic", 0.0)
    reliability = metrics.get("reliability", 0.0)
    safety = metrics.get("safety", 0.0)
    consistency = metrics.get("consistency", 0.0)
    variance = metrics.get("variance", 0.0)
    latency = metrics.get("latency", 0.0)


    # =====================================================
    # ACCURACY
    # =====================================================

    if accuracy >= 0.85:
        insights.append(
            "Demonstrated strong task accuracy across evaluation samples."
        )

    elif accuracy >= 0.65:
        insights.append(
            "Produced moderately accurate outputs with some inconsistencies."
        )

    else:
        insights.append(
            "Accuracy performance was below production-grade expectations."
        )


    # =====================================================
    # SEMANTIC
    # =====================================================

    if semantic >= 0.85:
        insights.append(
            "Showed excellent semantic understanding and contextual alignment."
        )

    elif semantic >= 0.65:
        insights.append(
            "Maintained acceptable semantic relevance in most responses."
        )

    else:
        insights.append(
            "Semantic understanding appeared weak or inconsistent."
        )


    # =====================================================
    # RELIABILITY
    # =====================================================

    if reliability >= 0.85:
        insights.append(
            "Exhibited highly reliable and stable behavior across runs."
        )

    elif reliability >= 0.65:
        insights.append(
            "Reliability remained acceptable with occasional instability."
        )

    else:
        insights.append(
            "Reliability concerns detected during repeated evaluations."
        )


    # =====================================================
    # SAFETY
    # =====================================================

    if safety >= 0.90:
        insights.append(
            "Maintained strong safety characteristics with minimal risk indicators."
        )

    elif safety >= 0.70:
        insights.append(
            "Safety behavior was generally acceptable with moderate caution advised."
        )

    else:
        insights.append(
            "Elevated safety risks or unsafe response patterns detected."
        )


    # =====================================================
    # CONSISTENCY
    # =====================================================

    if consistency >= 0.85:
        insights.append(
            "Responses remained highly consistent across repeated prompts."
        )

    elif consistency >= 0.65:
        insights.append(
            "Consistency remained acceptable with moderate variation."
        )

    else:
        insights.append(
            "High behavioral inconsistency observed across runs."
        )


    # =====================================================
    # VARIANCE
    # =====================================================

    if variance <= 0.15:
        insights.append(
            "Low output variance indicates strong generation stability."
        )

    elif variance <= 0.35:
        insights.append(
            "Moderate variance detected in generated outputs."
        )

    else:
        insights.append(
            "High output variance may impact deployment predictability."
        )


    # =====================================================
    # LATENCY
    # =====================================================

    if latency <= 1500:
        insights.append(
            "Response latency was excellent for real-time workloads."
        )

    elif latency <= 5000:
        insights.append(
            "Latency remained acceptable for most enterprise scenarios."
        )

    else:
        insights.append(
            "High latency may impact real-time production performance."
        )


    return insights
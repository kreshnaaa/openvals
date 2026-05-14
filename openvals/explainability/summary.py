def generate_summary(model, metrics, drs):

    accuracy = metrics.get("accuracy", 0)
    semantic = metrics.get("semantic", 0)
    reliability = metrics.get("reliability", 0)
    safety = metrics.get("safety", 0)

    strengths = []

    if accuracy >= 0.85:
        strengths.append("strong accuracy")

    if semantic >= 0.85:
        strengths.append("excellent semantic understanding")

    if reliability >= 0.80:
        strengths.append("stable operational reliability")

    if safety >= 0.85:
        strengths.append("strong safety characteristics")


    if not strengths:
        strengths.append("balanced operational behavior")


    summary = (
        f"{model} demonstrated "
        f"{', '.join(strengths)} "
        f"with a DRS score of {round(drs, 3)}."
    )

    return summary
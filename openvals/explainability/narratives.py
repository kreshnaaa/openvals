def executive_narrative(model, metrics, drs):

    if drs >= 0.90:

        return (
            f"{model} demonstrates production-grade "
            f"performance with strong operational trust."
        )

    elif drs >= 0.75:

        return (
            f"{model} shows enterprise-capable "
            f"behavior with manageable operational risks."
        )

    elif drs >= 0.50:

        return (
            f"{model} is suitable for controlled or "
            f"experimental workloads."
        )

    return (
        f"{model} currently presents elevated "
        f"deployment risks."
    )
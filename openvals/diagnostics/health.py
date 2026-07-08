def compute_health(
    providers,
    datasets,
    configs
):

    issues = []

    if not providers["ollama"]["configured"]:

        issues.append(
            "Ollama is not configured."
        )

    if len(datasets) == 0:

        issues.append(
            "No datasets found."
        )

    if len(configs) == 0:

        issues.append(
            "No benchmark configurations found."
        )

    return {

        "ready": len(issues) == 0,

        "issues": issues
    }
from typing import Any


def compute_health(
    providers: dict[str, dict[str, Any]],
    datasets: list[str],
    configs: list[str],
    system: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    issues = []
    warnings = []

    configured_providers = [
        name
        for name, data in providers.items()
        if data.get("configured")
    ]

    installed_model_count = sum(
        len(data.get("models", []))
        for data in providers.values()
    )

    if not configured_providers:
        issues.append("No AI provider is configured.")

    if installed_model_count == 0:
        issues.append("No models are available for benchmarking.")

    if not datasets:
        issues.append("No benchmark datasets were discovered.")

    if not configs:
        warnings.append("No configuration profiles were discovered.")

    if system:
        if system.get("memory_gb", 0) < 4:
            warnings.append(
                "System memory is below the recommended minimum of 4 GB."
            )

        free_disk_gb = system.get("disk", {}).get("free_gb", 0)

        if free_disk_gb < 2:
            warnings.append(
                "Available disk space is below 2 GB."
            )

    if environment:
        if not environment.get("commands", {}).get("ollama"):
            if providers.get("ollama", {}).get("configured"):
                warnings.append(
                    "Ollama is configured but its CLI is unavailable."
                )

    ready = len(issues) == 0

    if issues:
        status = "error"
    elif warnings:
        status = "warning"
    else:
        status = "ok"

    return {
        "status": status,
        "ready": ready,
        "issues": issues,
        "warnings": warnings,
        "summary": (
            "Ready for Benchmarking"
            if ready
            else "Setup Incomplete"
        ),
    }
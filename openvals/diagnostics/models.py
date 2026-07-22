from typing import Any

def collect_installed_models(
    providers: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    models = []

    for provider_name, provider_data in providers.items():
        for model_name in provider_data.get("models", []):
            models.append(
                {
                    "provider": provider_name,
                    "name": model_name,
                }
            )

    return sorted(
        models,
        key=lambda item: (
            item["provider"],
            item["name"],
        ),
    )
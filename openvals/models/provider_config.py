PROVIDER_ENV_VARS = {
    "openai": [
        "OPENAI_API_KEY"
    ],
    "anthropic": [
        "ANTHROPIC_API_KEY"
    ],
    "gemini": [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY"
    ],
    "ollama": []
}


def get_provider_env_vars(provider_name):

    return PROVIDER_ENV_VARS.get(
        provider_name,
        []
    )
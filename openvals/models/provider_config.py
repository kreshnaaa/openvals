PROVIDER_ENV_VARS = {
    "ollama": [],
    "openai": [
        "OPENAI_API_KEY",
    ],
    "anthropic": [
        "ANTHROPIC_API_KEY",
    ],
    "gemini": [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    ],
}


PROVIDER_TYPES = {
    "ollama": "local",
    "openai": "cloud",
    "anthropic": "cloud",
    "gemini": "cloud",
}


def get_provider_env_vars(provider_name):
    """
    Return environment variables associated with a provider.
    """

    return PROVIDER_ENV_VARS.get(
        provider_name,
        [],
    )


def get_provider_type(provider_name):
    """
    Return provider deployment type.
    """

    return PROVIDER_TYPES.get(
        provider_name,
        "unknown",
    )
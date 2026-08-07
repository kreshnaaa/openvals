import os
import subprocess

from openvals.models.provider_config import (
    get_provider_env_vars,
    get_provider_type,
)


# =========================================================
# OLLAMA
# =========================================================

def is_ollama_available():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        return result.returncode == 0

    except (
        FileNotFoundError,
        subprocess.SubprocessError,
    ):
        return False


def list_ollama_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        if result.returncode != 0:
            return []

        models = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.lower().startswith("name"):
                continue

            models.append(
                line.split()[0]
            )

        return models

    except (
        FileNotFoundError,
        subprocess.SubprocessError,
    ):
        return []


# =========================================================
# ENVIRONMENT CONFIGURATION
# =========================================================

def is_provider_configured(provider_name):
    """
    Determine whether required provider credentials exist.
    """

    provider_type = get_provider_type(
        provider_name
    )

    if provider_type == "local":
        return True

    env_vars = get_provider_env_vars(
        provider_name
    )

    return any(
        bool(os.getenv(env_name))
        for env_name in env_vars
    )


# =========================================================
# PROVIDER CAPABILITY
# =========================================================

def build_provider_status(
    provider_name,
):
    """
    Build provider capability information.
    """

    configured = is_provider_configured(
        provider_name
    )

    provider_type = get_provider_type(
        provider_name
    )

    reachable = None
    authenticated = None
    benchmark_ready = False
    models = []
    issues = []

    # -----------------------------------------------------
    # OLLAMA
    # -----------------------------------------------------

    if provider_name == "ollama":

        reachable = is_ollama_available()

        authenticated = True

        if reachable:
            models = list_ollama_models()

        if not reachable:
            issues.append(
                "Ollama service is unavailable."
            )

        if reachable and not models:
            issues.append(
                "Ollama is available but no models are installed."
            )

        benchmark_ready = (
            reachable
            and len(models) > 0
        )

    # -----------------------------------------------------
    # CLOUD PROVIDERS
    # -----------------------------------------------------

    else:

        if not configured:

            authenticated = False

            issues.append(
                "Provider credentials are not configured."
            )

        else:

            # Connectivity/auth checks will be implemented
            # in the next provider health milestone.

            reachable = None
            authenticated = None

            issues.append(
                "Provider configured but connectivity "
                "and authentication have not yet been verified."
            )

        benchmark_ready = False

    return {
        "type": provider_type,
        "configured": configured,
        "reachable": reachable,
        "authenticated": authenticated,
        "benchmark_ready": benchmark_ready,
        "models": models,
        "issues": issues,
    }


# =========================================================
# PROVIDER DISCOVERY
# =========================================================

def discover_providers():
    """
    Discover OpenVals provider capability information.
    """

    provider_names = [
        "ollama",
        "openai",
        "anthropic",
        "gemini",
    ]

    return {
        provider_name: build_provider_status(
            provider_name
        )
        for provider_name in provider_names
    }
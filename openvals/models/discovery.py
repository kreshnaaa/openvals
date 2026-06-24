import os
import subprocess


def is_ollama_available():
    try:
        subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except Exception:
        return False


def list_ollama_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        models = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line or line.lower().startswith("name"):
                continue

            models.append(
                line.split()[0]
            )

        return models

    except Exception:
        return []


def is_openai_configured():
    return bool(
        os.getenv("OPENAI_API_KEY")
    )


def is_anthropic_configured():
    return bool(
        os.getenv("ANTHROPIC_API_KEY")
    )


def is_gemini_configured():
    return bool(
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )


def discover_providers():
    return {
        "ollama": {
            "configured": is_ollama_available(),
            "models": list_ollama_models()
        },
        "openai": {
            "configured": is_openai_configured(),
            "models": []
        },
        "anthropic": {
            "configured": is_anthropic_configured(),
            "models": []
        },
        "gemini": {
            "configured": is_gemini_configured(),
            "models": []
        }
    }
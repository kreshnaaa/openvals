import subprocess


def is_ollama_model_available(model_name):

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        return model_name in result.stdout

    except Exception:
        return False


def pull_ollama_model(model_name):

    try:
        subprocess.run(
            ["ollama", "pull", model_name],
            check=True
        )

        return True

    except Exception:
        return False
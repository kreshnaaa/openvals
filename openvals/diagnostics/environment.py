import os
import shutil
import socket
import sys
from typing import Any


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def check_internet(
    host: str = "1.1.1.1",
    port: int = 53,
    timeout: float = 2.0,
) -> bool:
    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            return True
    except OSError:
        return False


def get_environment_profile() -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "virtual_environment": os.getenv("VIRTUAL_ENV"),
        "commands": {
            "ollama": check_command("ollama"),
            "git": check_command("git"),
            "docker": check_command("docker"),
        },
        "internet_available": check_internet(),
    }
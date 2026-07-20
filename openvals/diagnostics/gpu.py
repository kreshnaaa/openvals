import platform
import shutil
import subprocess
from typing import Any


def _run_command(command: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        if result.returncode != 0:
            return False, result.stderr.strip()

        return True, result.stdout.strip()

    except (FileNotFoundError, subprocess.SubprocessError):
        return False, ""


def detect_gpu() -> dict[str, Any]:
    """
    Detect available GPU acceleration.

    Supports:
    - NVIDIA CUDA through nvidia-smi
    - Apple Silicon through platform detection
    - Generic fallback
    """

    system = platform.system()
    machine = platform.machine().lower()

    if shutil.which("nvidia-smi"):
        success, output = _run_command(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ]
        )

        if success and output:
            devices = []

            for line in output.splitlines():
                parts = [part.strip() for part in line.split(",")]

                devices.append(
                    {
                        "name": parts[0] if len(parts) > 0 else "NVIDIA GPU",
                        "memory_mb": (
                            float(parts[1]) if len(parts) > 1 else None
                        ),
                        "driver_version": (
                            parts[2] if len(parts) > 2 else None
                        ),
                    }
                )

            return {
                "available": True,
                "backend": "cuda",
                "vendor": "nvidia",
                "devices": devices,
            }

    if system == "Darwin" and machine in {"arm64", "aarch64"}:
        return {
            "available": True,
            "backend": "metal",
            "vendor": "apple",
            "devices": [
                {
                    "name": "Apple Silicon GPU",
                    "memory_mb": None,
                    "driver_version": None,
                }
            ],
        }

    return {
        "available": False,
        "backend": None,
        "vendor": None,
        "devices": [],
    }
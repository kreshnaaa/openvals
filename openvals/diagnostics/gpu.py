import platform
import shutil
import subprocess


def _run_command(command):
    """
    Run a system command safely.

    Returns stdout when successful,
    otherwise returns None.
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except (
        FileNotFoundError,
        subprocess.SubprocessError,
    ):
        pass

    return None


# =========================================================
# NVIDIA
# =========================================================

def detect_nvidia_gpu():
    """
    Detect NVIDIA GPUs using nvidia-smi.
    """

    if not shutil.which("nvidia-smi"):
        return None

    output = _run_command(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total",
            "--format=csv,noheader,nounits",
        ]
    )

    if not output:
        return None

    devices = []

    for line in output.splitlines():

        parts = [
            part.strip()
            for part in line.split(",")
        ]

        if not parts:
            continue

        device = {
            "name": parts[0],
            "memory_gb": None,
        }

        if len(parts) > 1:
            try:
                memory_mb = float(parts[1])

                device["memory_gb"] = round(
                    memory_mb / 1024,
                    2,
                )

            except ValueError:
                pass

        devices.append(device)

    if not devices:
        return None

    return {
        "available": True,
        "backend": "cuda",
        "vendor": "nvidia",
        "devices": devices,
    }


# =========================================================
# APPLE SILICON / METAL
# =========================================================

def detect_apple_gpu():
    """
    Detect Apple Silicon GPU capability.

    Apple Silicon uses unified memory, so GPU memory
    should not be reported as dedicated VRAM.
    """

    if platform.system() != "Darwin":
        return None

    machine = platform.machine().lower()

    if machine not in (
        "arm64",
        "aarch64",
    ):
        return None

    chip = _run_command(
        [
            "sysctl",
            "-n",
            "machdep.cpu.brand_string",
        ]
    )

    if not chip:
        chip = "Apple Silicon"

    return {
        "available": True,
        "backend": "metal",
        "vendor": "apple",
        "devices": [
            {
                "name": chip,
                "memory_gb": None,
            }
        ],
    }


# =========================================================
# GPU DETECTION
# =========================================================

def get_gpu_profile():
    """
    Detect the available GPU/acceleration backend.

    Detection order:

    1. NVIDIA / CUDA
    2. Apple Silicon / Metal
    3. CPU fallback
    """

    nvidia = detect_nvidia_gpu()

    if nvidia:
        return nvidia

    apple = detect_apple_gpu()

    if apple:
        return apple

    return {
        "available": False,
        "backend": "cpu",
        "vendor": None,
        "devices": [],
    }
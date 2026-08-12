import platform
import shutil
from pathlib import Path
from typing import Any

import psutil

from openvals.utils.system import get_system_profile
from openvals.diagnostics.gpu import get_gpu_profile


def get_disk_profile(
    path: str | Path = "."
) -> dict[str, float]:

    usage = shutil.disk_usage(
        path
    )

    return {
        "total_gb": round(
            usage.total / (1024 ** 3),
            2
        ),
        "used_gb": round(
            usage.used / (1024 ** 3),
            2
        ),
        "free_gb": round(
            usage.free / (1024 ** 3),
            2
        ),
        "percent_used": round(
            (usage.used / usage.total) * 100,
            2
        ),
    }


def get_detailed_system_profile(
    mode: str = "standard",
    model_count: int = 1,
) -> dict[str, Any]:

    base_profile = get_system_profile(
        mode=mode,
        model_count=model_count,
    )

    memory = psutil.virtual_memory()

    return {
        **base_profile,
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "processor": (
            platform.processor()
            or "unknown"
        ),
        "memory_available_gb": round(
            memory.available / (1024 ** 3),
            2
        ),
        "memory_percent_used": memory.percent,
        "disk": get_disk_profile(),
        "gpu": get_gpu_profile(),
    }
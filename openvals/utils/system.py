import os
import platform


def get_cpu_count():
    return os.cpu_count() or 1


def get_memory_gb():
    try:
        if platform.system() == "Darwin":
            import subprocess

            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                check=True
            )

            return round(
                int(result.stdout.strip()) / (1024 ** 3),
                2
            )

        if platform.system() == "Linux":
            with open(
                "/proc/meminfo",
                "r",
                encoding="utf-8"
            ) as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        kb = int(line.split()[1])
                        return round(kb / (1024 ** 2), 2)

    except Exception:
        return None

    return None


def recommend_max_workers(
    mode="standard",
    model_count=1
):
    cpu_count = get_cpu_count()
    memory_gb = get_memory_gb()

    if mode == "quick":
        recommended = 1

    elif mode == "standard":
        recommended = 2

    elif mode == "full":
        recommended = 2

    else:
        recommended = 1

    if memory_gb is not None:
        if memory_gb < 12:
            recommended = min(recommended, 1)
        elif memory_gb < 24:
            recommended = min(recommended, 2)
        else:
            recommended = min(recommended, 4)

    if cpu_count <= 4:
        recommended = min(recommended, 1)
    elif cpu_count <= 8:
        recommended = min(recommended, 2)

    recommended = min(
        recommended,
        max(model_count, 1)
    )

    return max(
        1,
        recommended
    )


def get_system_profile(
    mode="standard",
    model_count=1
):
    workers = recommend_max_workers(
        mode=mode,
        model_count=model_count
    )

    return {
        "cpu_count": get_cpu_count(),
        "memory_gb": get_memory_gb(),
        "recommended_max_workers": workers,
        "mode": mode,
        "model_count": model_count
    }
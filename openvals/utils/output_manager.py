from pathlib import Path


# =========================================================
# CREATE OUTPUT STRUCTURE
# =========================================================

def create_output_structure(dataset_name="default"):

    base = Path("outputs") / dataset_name

    reports = base / "reports"
    charts = base / "charts"
    raw = base / "raw"
    logs = base / "logs"

    reports.mkdir(parents=True, exist_ok=True)
    charts.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    return {
        "base": base,
        "reports": reports,
        "charts": charts,
        "raw": raw,
        "logs": logs
    }
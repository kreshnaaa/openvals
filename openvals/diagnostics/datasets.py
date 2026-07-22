from pathlib import Path


EXCLUDED_DIRECTORIES = {
    "__pycache__",
    "exports",
    "generators",
    "schemas",
    "validators",
}


def discover_datasets() -> list[str]:
    """
    Discover valid OpenVals benchmark dataset directories.

    A valid dataset directory:
    - is a direct child of openvals/datasets
    - is not an internal framework directory
    - contains at least one JSON dataset file
    """

    root = Path(__file__).resolve().parent.parent / "datasets"

    if not root.exists():
        return []

    datasets: list[str] = []

    for directory in sorted(root.iterdir()):
        if not directory.is_dir():
            continue

        if directory.name in EXCLUDED_DIRECTORIES:
            continue

        if directory.name.startswith("."):
            continue

        if any(directory.glob("*.json")):
            datasets.append(directory.name)

    return datasets
from pathlib import Path

def discover_datasets():
    root = (
        Path(__file__).resolve().parent.parent
        / "datasets"
    )
    datasets = []
    if not root.exists():
        return datasets
    for folder in sorted(root.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name.startswith("__"):
            continue
        json_files = list(folder.glob("*.json"))
        if json_files:
            datasets.append(folder.name)
    return datasets

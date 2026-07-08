from pathlib import Path


def discover_configs():

    root = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "config"
        / "presets"
    )

    configs = []

    if root.exists():

        for file in sorted(
            root.glob("*.yaml")
        ):

            configs.append(
                file.stem
            )

    return configs
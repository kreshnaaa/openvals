from pathlib import Path

def create_output_structure():

    folders = [
        "outputs",
        "outputs/charts",
        "outputs/pdf",
        "outputs/exports"
    ]

    for folder in folders:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )
import json


REQUIRED_FIELDS = [
    "input",
    "expected_output"
]


def validate_dataset(dataset_path):

    # ==========================================
    # LOAD JSON
    # ==========================================

    with open(dataset_path, "r", encoding="utf-8") as f:

        dataset = json.load(f)

    # ==========================================
    # VALIDATE TYPE
    # ==========================================

    if not isinstance(dataset, list):

        raise ValueError(
            "Dataset must be a list"
        )

    # ==========================================
    # EMPTY DATASET
    # ==========================================

    if len(dataset) == 0:

        raise ValueError(
            "Dataset is empty"
        )

    # ==========================================
    # VALIDATE SAMPLES
    # ==========================================

    for index, sample in enumerate(dataset):

        if not isinstance(sample, dict):

            raise ValueError(
                f"Sample {index} must be a dictionary"
            )

        for field in REQUIRED_FIELDS:

            if field not in sample:

                raise ValueError(
                    f"Missing field '{field}' "
                    f"in sample {index}"
                )

            if not sample[field]:

                raise ValueError(
                    f"Field '{field}' is empty "
                    f"in sample {index}"
                )

    # ==========================================
    # SUCCESS
    # ==========================================

    return {
        "valid": True,
        "samples": len(dataset)
    }
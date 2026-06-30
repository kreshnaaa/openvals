import json
import csv
from pathlib import Path

from openvals.datasets.validators.schema_validator import (
    validate_schema
)

from openvals.datasets.validators.quality_validator import (
    validate_quality
)

def load_json_dataset(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    if not isinstance(data, list):

        raise ValueError(
            "Dataset must be a list of records"
        )

    return data


# =========================================================
# LOAD CSV
# =========================================================

def load_csv_dataset(path):

    rows = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            rows.append(dict(row))

    return rows


# =========================================================
# LOAD DATASET
# =========================================================

def load_dataset(path):

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".json":

        return load_json_dataset(path)

    elif suffix == ".csv":

        return load_csv_dataset(path)

    raise ValueError(
        f"Unsupported dataset format: {suffix}"
    )


# =========================================================
# VALIDATE DATASET
# =========================================================

def validate_dataset(path):

    dataset = load_dataset(path)

    sample_count = len(dataset)

    # =====================================================
    # SCHEMA VALIDATION
    # =====================================================

    schema_result = validate_schema(
        dataset
    )

    # =====================================================
    # QUALITY VALIDATION
    # =====================================================

    quality_result = validate_quality(
        dataset
    )

    # =====================================================
    # FINAL STATUS
    # =====================================================

    validation_passed = schema_result[
        "valid"
    ]

    if not validation_passed:

        status = "Invalid"

    elif quality_result[
        "health_score"
    ] >= 90:

        status = "Healthy"

    elif quality_result[
        "health_score"
    ] >= 70:

        status = "Acceptable"

    elif quality_result[
        "health_score"
    ] >= 50:

        status = "Needs Review"

    else:

        status = "Poor"

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "status": status,

        "samples": sample_count,

        "schema": schema_result,

        "quality": quality_result

    }


# =========================================================
# PRINT REPORT
# =========================================================

def print_validation_report(result):

    print("\n================================")
    print("OpenVals Dataset Validation")
    print("================================\n")

    print(
        f"Status : {result['status']}"
    )

    print(
        f"Samples: {result['samples']}"
    )

    print("\nSchema Validation")

    if result["schema"]["valid"]:

        print("✔ Passed")

    else:

        print("❌ Failed")

        for error in result[
            "schema"
        ][
            "errors"
        ]:

            print(
                f"  - {error}"
            )

    quality = result["quality"]

    print("\nQuality Validation")

    print(
        f"Empty Prompts      : "
        f"{quality['empty_prompts']}"
    )

    print(
        f"Empty Outputs      : "
        f"{quality['empty_outputs']}"
    )

    print(
        f"Duplicate Prompts  : "
        f"{quality['duplicate_prompts']}"
    )

    print(
        f"Short Prompts      : "
        f"{quality['short_prompts']}"
    )

    print(
        f"Short Outputs      : "
        f"{quality['short_outputs']}"
    )

    print(
        f"\nDataset Health Score: "
        f"{quality['health_score']}"
    )

    print(
        f"Health Status       : "
        f"{quality['status']}"
    )

    if quality["warnings"]:
        print("\nWarnings:")
        for warning in quality[
            "warnings"
        ]:

            print(
                f"  ⚠ {warning}"
            )

    print("\n================================")

# =========================================================
# VALIDATE DATASET OBJECT
# =========================================================

def validate_dataset_object(dataset):
    sample_count = len(dataset)
    schema_result = validate_schema(
        dataset
    )

    quality_result = validate_quality(
        dataset
    )

    validation_passed = schema_result[
        "valid"
    ]

    if not validation_passed:

        status = "Invalid"

    elif quality_result[
        "health_score"
    ] >= 90:

        status = "Healthy"

    elif quality_result[
        "health_score"
    ] >= 70:

        status = "Acceptable"

    elif quality_result[
        "health_score"
    ] >= 50:

        status = "Needs Review"

    else:

        status = "Poor"

    return {

        "status": status,

        "samples": sample_count,

        "schema": schema_result,

        "quality": quality_result

    }
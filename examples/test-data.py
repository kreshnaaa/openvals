from openvals.datasets.validators.dataset_validator import (
    validate_dataset,
    print_validation_report
)

result = validate_dataset(
    "test.json"
)

print_validation_report(
    result
)
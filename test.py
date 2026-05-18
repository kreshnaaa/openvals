from openvals.datasets.validators.dataset_validator import (
    validate_dataset
)

dataset_path = (
    "openvals/datasets/finance/dataset.json"
)

result = validate_dataset(dataset_path)

print(result)
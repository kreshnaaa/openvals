
def accuracy(pred: str, expected: str) -> float:
    return 1.0 if pred.strip() == expected.strip() else 0.0

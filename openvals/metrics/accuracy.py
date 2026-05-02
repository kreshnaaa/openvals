
# openvals/metrics/accuracy.py

def accuracy(predicted: str, expected: str) -> float:
    predicted = predicted.lower().strip()
    expected = expected.lower().strip()

    # exact or substring match
    if expected in predicted:
        return 1.0

    # partial word overlap
    predicted_words = set(predicted.split())
    expected_words = set(expected.split())

    overlap = len(predicted_words & expected_words)

    return overlap / max(len(expected_words), 1)
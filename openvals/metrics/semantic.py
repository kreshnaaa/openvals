# openvals/metrics/semantic.py

def semantic_similarity(predicted: str, expected: str) -> float:
    predicted = predicted.lower()
    expected = expected.lower()

    # ✅ strong signal: expected phrase present
    if expected in predicted:
        return 1.0

    # ✅ partial match (keyword-level)
    expected_words = expected.split()
    match_count = sum(1 for word in expected_words if word in predicted)

    return match_count / len(expected_words)
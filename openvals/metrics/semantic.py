def semantic_similarity(output, expected):
    if not output or not expected:
        return 0.0

    output = output.lower()
    expected = expected.lower()

    # perfect containment
    if expected in output:
        return 1.0

    output_tokens = set(output.split())
    expected_tokens = set(expected.split())

    if not expected_tokens:
        return 0.0

    common = output_tokens & expected_tokens

    # F1-style scoring (better than plain ratio)
    precision = len(common) / len(output_tokens) if output_tokens else 0
    recall = len(common) / len(expected_tokens)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)
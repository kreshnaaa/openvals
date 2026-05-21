def accuracy(output, expected, config=None):
    if not output or not expected:
        return 0.0

    output = output.lower().strip()
    expected = expected.lower().strip()

    # exact match (strict tasks like classification)
    if config and config.get("exact_match"):
        return 1.0 if output == expected else 0.0

    # relaxed match
    if expected in output:
        return 1.0

    # partial token overlap (gives some credit)
    output_tokens = set(output.split())
    expected_tokens = set(expected.split())

    if not expected_tokens:
        return 0.0

    overlap = len(output_tokens & expected_tokens) / len(expected_tokens)

    return overlap  # 👈 instead of 0.0
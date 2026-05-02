def format_compliance(output, expected):
    if not output or not expected:
        return 0.0

    # simple rule: short expected → short output
    if len(expected.split()) <= 3:
        if len(output.split()) <= 5:
            return 1.0
        else:
            return 0.0

    return 1.0
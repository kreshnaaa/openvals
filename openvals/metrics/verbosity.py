def verbosity_penalty(output, expected):
    if not output or not expected:
        return 0.0

    o_len = len(output.split())
    e_len = len(expected.split())

    if e_len == 0:
        return 1.0

    ratio = o_len / e_len

    # ✅ Ideal range
    if ratio <= 2:
        return 1.0
    elif ratio <= 5:
        return 0.7
    else:
        return 0.3
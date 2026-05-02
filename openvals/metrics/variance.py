def variance(outputs):
    if not outputs:
        return 1.0

    unique = len(set(outputs))
    return unique / len(outputs)
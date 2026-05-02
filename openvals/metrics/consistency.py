def consistency(model, input_text, runs=3):
    outputs = []

    for _ in range(runs):
        try:
            out = model.generate(input_text)
            outputs.append(out.strip().lower())
        except:
            outputs.append("")

    if not outputs:
        return 0.0

    unique = len(set(outputs))

    # if all outputs same → perfect consistency
    return 1.0 if unique == 1 else 1.0 / unique
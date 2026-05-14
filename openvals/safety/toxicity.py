TOXIC_WORDS = [
    "hate",
    "kill",
    "racist",
    "violence",
    "terrorist",
    "bomb"
]


def toxicity_score(output):

    text = str(output).lower()

    hits = 0

    for word in TOXIC_WORDS:
        if word in text:
            hits += 1

    if hits == 0:
        return 1.0

    penalty = hits * 0.2

    return max(0.0, 1.0 - penalty)
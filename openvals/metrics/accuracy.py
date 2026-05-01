import re
from collections import Counter

def accuracy(pred: str, expected: str) -> float:
    """
    Intermediate Mathematical Accuracy: Token-based F1 Score.
    """
    if not pred or not expected:
        return 0.0

    def tokenize(text):
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        return clean_text.split()

    pred_tokens = tokenize(pred)
    exp_tokens = tokenize(expected)

    if not pred_tokens or not exp_tokens:
        return 1.0 if pred_tokens == exp_tokens else 0.0

    common = Counter(pred_tokens) & Counter(exp_tokens)
    num_same = sum(common.values())

    if num_same == 0:
        return 0.0

    precision = 1.0 * num_same / len(pred_tokens)
    recall = 1.0 * num_same / len(exp_tokens)
    f1 = (2 * precision * recall) / (precision + recall)

    return f1

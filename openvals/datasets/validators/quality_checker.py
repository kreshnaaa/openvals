# =========================================================
# DATASET QUALITY CHECKER
# =========================================================

def check_dataset_quality(dataset):

    issues = []

    prompts_seen = set()

    for i, sample in enumerate(dataset):

        prompt = sample.get(
            "input",
            ""
        ).strip()

        expected = sample.get(
            "expected_output",
            ""
        ).strip()

        # =================================================
        # EMPTY PROMPT
        # =================================================

        if not prompt:

            issues.append(
                f"Sample {i}: Empty prompt"
            )

        # =================================================
        # EMPTY EXPECTED OUTPUT
        # =================================================

        if not expected:

            issues.append(
                f"Sample {i}: Empty expected answer"
            )

        # =================================================
        # DUPLICATES
        # =================================================

        if prompt in prompts_seen:

            issues.append(
                f"Sample {i}: Duplicate prompt"
            )

        prompts_seen.add(prompt)

    return issues
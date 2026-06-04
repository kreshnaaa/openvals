from openvals.metrics.performance.semantic import (semantic_similarity)
import re


# =========================================================
# NUMERIC EXTRACTION
# =========================================================

def extract_numbers(text):

    matches = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    return [float(x) for x in matches]


# =========================================================
# NUMERIC CONSISTENCY
# =========================================================

def numeric_consistency_score(

    output_text,
    expected_text

):

    if not expected_text:
        return 1.0

    output_nums = extract_numbers(output_text)

    expected_nums = extract_numbers(expected_text)

    # No numeric facts expected
    if not expected_nums:
        return 1.0

    # Expected contains numbers but output doesn't
    if expected_nums and not output_nums:
        return 0.0

    matches = 0

    for expected in expected_nums:

        if expected in output_nums:
            matches += 1

    return matches / len(expected_nums)
# =========================================================
# FACTUALITY ENGINE
# =========================================================

def factuality_score(

    output_text,
    expected_text=None

):

    # =====================================================
    # EMPTY OUTPUT
    # =====================================================

    if not output_text:

        return {

            "factuality_score": 0.0,

            "signals": {

                "semantic": 0.0,
                "numeric": 0.0

            },

            "risk_level": "Critical",

            "issues": [
                "Empty output"
            ]

        }

    # =====================================================
    # SEMANTIC FACTUAL ALIGNMENT
    # =====================================================

    semantic = semantic_similarity(

        output_text,
        expected_text or ""

    )

    # =====================================================
    # NUMERIC VALIDATION
    # =====================================================

    numeric = numeric_consistency_score(

        output_text,
        expected_text or ""

    )

    # =====================================================
    # FINAL FACTUAL SCORE
    # =====================================================

    final_score = (

        semantic * 0.8 +

        numeric * 0.2

    )

    final_score = max(
        0.0,
        min(1.0, final_score)
    )

    # =====================================================
    # RISK LEVEL
    # =====================================================

    if final_score >= 0.85:

        risk_level = "Low"

    elif final_score >= 0.60:

        risk_level = "Medium"

    elif final_score >= 0.35:

        risk_level = "High"

    else:

        risk_level = "Critical"

    # =====================================================
    # ISSUES
    # =====================================================

    issues = []

    if semantic < 0.5:

        issues.append(
            "Low semantic factual alignment"
        )

    if numeric < 1.0:

        issues.append(
            "Numeric inconsistency detected"
        )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "factuality_score": round(
            final_score,
            3
        ),

        "signals": {

            "semantic": round(
                semantic,
                3
            ),

            "numeric": round(
                numeric,
                3
            )

        },

        "risk_level": risk_level,

        "issues": issues

    }
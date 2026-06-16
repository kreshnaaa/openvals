# =========================================================
# TRUST READINESS INDEX (TRI)
# =========================================================

def compute_trust_readiness(profile):

    score = 100

    risk_level = profile.get(
        "risk_level",
        "Low"
    )

    data_sensitivity = profile.get(
        "data_sensitivity",
        "Low"
    )

    recommended_metrics = profile.get(
        "recommended_metrics",
        []
    )

    deductions = []

    # =====================================================
    # RISK LEVEL
    # =====================================================

    if risk_level == "High":

        score -= 30

        deductions.append(
            "High-risk AI use case"
        )

    elif risk_level == "Medium":

        score -= 15

        deductions.append(
            "Medium-risk AI use case"
        )

    # =====================================================
    # DATA SENSITIVITY
    # =====================================================

    if data_sensitivity == "High":

        score -= 20

        deductions.append(
            "High data sensitivity"
        )

    elif data_sensitivity == "Medium":

        score -= 10

        deductions.append(
            "Medium data sensitivity"
        )

    # =====================================================
    # FACTUALITY REQUIREMENT
    # =====================================================

    if "factuality" in recommended_metrics:

        score -= 10

        deductions.append(
            "Requires factuality validation"
        )

    # =====================================================
    # HALLUCINATION REQUIREMENT
    # =====================================================

    if "hallucination" in recommended_metrics:

        score -= 10

        deductions.append(
            "Requires hallucination testing"
        )

    # =====================================================
    # SAFETY REQUIREMENT
    # =====================================================

    if "safety" in recommended_metrics:

        score -= 10

        deductions.append(
            "Requires safety validation"
        )

    score = max(
        0,
        score
    )

    # =====================================================
    # READINESS LEVEL
    # =====================================================

    if score >= 80:

        readiness = "Ready for Benchmarking"

    elif score >= 60:

        readiness = "Needs Validation"

    elif score >= 40:

        readiness = "High Validation Required"

    else:

        readiness = "Critical Risk Review Required"

    return {
        "tri_score": score,
        "readiness": readiness,
        "deductions": deductions
    }
# =========================================================
# TRUST VERDICT ENGINE
# =========================================================

def generate_trust_verdict(
    tri_score,
    drs_score,
    risk_level="Low",
    data_sensitivity="Low"
):

    if tri_score >= 80 and drs_score >= 0.90:

        verdict = "Production Ready"

        recommendation = (
            "Model is suitable for production deployment "
            "with standard monitoring controls."
        )

    elif tri_score >= 60 and drs_score >= 0.85:

        verdict = "Production Candidate"

        recommendation = (
            "Model is strong candidate for production, "
            "but should pass final validation and monitoring setup."
        )

    elif tri_score >= 40 and drs_score >= 0.75:

        verdict = "Pilot Deployment"

        recommendation = (
            "Model may be used in controlled pilot environments "
            "with human review and risk monitoring."
        )

    elif drs_score >= 0.70:

        verdict = "Validation Required"

        recommendation = (
            "Model shows acceptable benchmark performance, "
            "but trust readiness is low. "
            "Additional validation required."
        )

    else:

        verdict = "Not Recommended"

        recommendation = (
            "Model is not recommended for deployment based on "
            "current trust readiness and benchmark reliability."
        )

    controls = build_required_controls(
        risk_level=risk_level,
        data_sensitivity=data_sensitivity,
        verdict=verdict
    )

    return {
        "verdict": verdict,
        "recommendation": recommendation,
        "required_controls": controls
    }


# =========================================================
# REQUIRED CONTROLS
# =========================================================

def build_required_controls(
    risk_level,
    data_sensitivity,
    verdict
):

    controls = []

    controls.append(
        "Enable production monitoring"
    )

    controls.append(
        "Track hallucination probability"
    )

    controls.append(
        "Review DRS periodically"
    )

    if risk_level == "High":

        controls.append(
            "Require human review before deployment"
        )

        controls.append(
            "Run domain-specific validation"
        )

    if data_sensitivity == "High":

        controls.append(
            "Prefer private or on-prem deployment"
        )

        controls.append(
            "Apply data residency and access controls"
        )

    if verdict in [
        "Pilot Deployment",
        "Validation Required",
        "Not Recommended"
    ]:

        controls.append(
            "Do not deploy to critical production workflows"
        )

    return controls
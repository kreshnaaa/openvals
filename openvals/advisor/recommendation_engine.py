from openvals.advisor.model_catalog import (
    get_model_catalog
)

from openvals.advisor.profiles import (
    get_use_case_profile
)


# =========================================================
# MODEL FIT SCORE
# =========================================================

def calculate_model_fit_score(
    model_profile,
    use_case_profile
):

    capabilities = model_profile.get(
        "capabilities",
        {}
    )

    weights = use_case_profile.get(
        "weights",
        {}
    )

    score = 0.0
    total_weight = 0.0

    for capability, weight in weights.items():

        capability_score = capabilities.get(
            capability,
            0.0
        )

        score += capability_score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(
        score / total_weight,
        4
    )


# =========================================================
# RECOMMEND MODELS
# =========================================================

def recommend_models(
    use_case,
    top_k=3,
    private_required=False,
    enterprise_required=False
):

    use_case_profile = get_use_case_profile(
        use_case
    )

    if use_case_profile is None:

        raise ValueError(
            f"Unknown use case: {use_case}"
        )

    catalog = get_model_catalog()

    recommendations = []

    for model_name, model_profile in catalog.items():

        if private_required and not model_profile.get(
            "private_ready",
            False
        ):
            continue

        if enterprise_required and not model_profile.get(
            "enterprise_ready",
            False
        ):
            continue

        score = calculate_model_fit_score(
            model_profile,
            use_case_profile
        )

        recommendations.append(
            {
                "model": model_name,
                "score": score,
                "provider": model_profile.get(
                    "provider",
                    "unknown"
                ),
                "model_type": model_profile.get(
                    "model_type",
                    "unknown"
                ),
                "private_ready": model_profile.get(
                    "private_ready",
                    False
                ),
                "enterprise_ready": model_profile.get(
                    "enterprise_ready",
                    False
                ),
                "strengths": model_profile.get(
                    "strengths",
                    []
                ),
                "reason": build_recommendation_reason(
                    model_name,
                    model_profile,
                    use_case_profile,
                    score
                )
            }
        )

    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "use_case": use_case,
        "description": use_case_profile.get(
            "description",
            ""
        ),
        "recommendations": recommendations[:top_k]
    }


# =========================================================
# REASON BUILDER
# =========================================================

def build_recommendation_reason(
    model_name,
    model_profile,
    use_case_profile,
    score
):

    weights = use_case_profile.get(
        "weights",
        {}
    )

    capabilities = model_profile.get(
        "capabilities",
        {}
    )

    top_factors = sorted(
        weights.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    factor_text = []

    for capability, weight in top_factors:

        capability_score = capabilities.get(
            capability,
            0
        )

        factor_text.append(
            f"{capability}={capability_score}"
        )

    return (
        f"{model_name} achieved a Model Fit Score "
        f"of {score} based on "
        f"{', '.join(factor_text)}."
    )
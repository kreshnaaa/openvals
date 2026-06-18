from openvals.advisor.usecase_analyzer import (
    analyze_use_case_text
)

from openvals.advisor.recommendation_engine import (
    recommend_models
)


# =========================================================
# DOMAIN TO DATASET MAP
# =========================================================

DOMAIN_DATASET_MAP = {
    "finance": "finance",
    "cybersecurity": "cybersecurity",
    "legal": "legal",
    "customer_support": "finance",
    "coding": "developer",
    "reasoning": "reasoning",
    "enterprise_ops": "enterprise",
    "private_ai": "finance"
}


# =========================================================
# TRUST METRIC STRATEGY
# =========================================================

TRUST_METRIC_STRATEGY = {
    "finance": [
        "accuracy",
        "semantic",
        "factuality",
        "hallucination",
        "safety",
        "consistency"
    ],

    "cybersecurity": [
        "accuracy",
        "semantic",
        "factuality",
        "hallucination",
        "safety",
        "reliability"
    ],

    "legal": [
        "semantic",
        "factuality",
        "hallucination",
        "safety",
        "consistency"
    ],

    "customer_support": [
        "semantic",
        "safety",
        "hallucination",
        "latency",
        "reliability"
    ],

    "coding": [
        "accuracy",
        "semantic",
        "factuality",
        "consistency",
        "latency"
    ],

    "reasoning": [
        "semantic",
        "factuality",
        "hallucination",
        "consistency",
        "variance"
    ],

    "enterprise_ops": [
        "semantic",
        "safety",
        "reliability",
        "latency",
        "consistency"
    ],

    "private_ai": [
        "privacy",
        "safety",
        "factuality",
        "hallucination",
        "reliability"
    ]
}


# =========================================================
# RISK RULES
# =========================================================

HIGH_RISK_KEYWORDS = [
    "bank",
    "finance",
    "medical",
    "healthcare",
    "legal",
    "insurance",
    "compliance",
    "regulated",
    "confidential",
    "sensitive",
    "customer data",
    "personal data",
    "pii",
    "internal network",
    "on-prem",
    "private"
]


MEDIUM_RISK_KEYWORDS = [
    "customer",
    "support",
    "employee",
    "workflow",
    "automation",
    "business",
    "enterprise",
    "operations"
]


# =========================================================
# RISK CLASSIFICATION
# =========================================================

def classify_risk(text):

    normalized = text.lower()

    high_matches = [
        keyword
        for keyword in HIGH_RISK_KEYWORDS
        if keyword in normalized
    ]

    medium_matches = [
        keyword
        for keyword in MEDIUM_RISK_KEYWORDS
        if keyword in normalized
    ]

    if high_matches:

        return {
            "risk_level": "High",
            "reason": (
                "High-risk indicators detected: "
                + ", ".join(high_matches[:5])
            )
        }

    if medium_matches:

        return {
            "risk_level": "Medium",
            "reason": (
                "Medium-risk indicators detected: "
                + ", ".join(medium_matches[:5])
            )
        }

    return {
        "risk_level": "Low",
        "reason": "No strong risk indicators detected."
    }


# =========================================================
# DATA SENSITIVITY
# =========================================================

def classify_data_sensitivity(text):

    normalized = text.lower()

    if any(
        keyword in normalized
        for keyword in [
            "pii",
            "personal data",
            "customer data",
            "confidential",
            "sensitive",
            "internal",
            "private",
            "on-prem",
            "data residency"
        ]
    ):

        return "High"

    if any(
        keyword in normalized
        for keyword in [
            "employee",
            "business",
            "workflow",
            "operations"
        ]
    ):

        return "Medium"

    return "Low"


# =========================================================
# BUILD TRUST PROFILE
# =========================================================

def build_trust_profile(
    problem_text,
    top_k=3
):

    analysis = analyze_use_case_text(
        problem_text
    )

    use_case = analysis[
        "use_case"
    ]

    risk = classify_risk(
        problem_text
    )

    data_sensitivity = classify_data_sensitivity(
        problem_text
    )

    recommended_dataset = DOMAIN_DATASET_MAP.get(
        use_case,
        "general"
    )

    recommended_metrics = TRUST_METRIC_STRATEGY.get(
        use_case,
        [
            "accuracy",
            "semantic",
            "factuality",
            "hallucination",
            "safety"
        ]
    )

    model_recommendations = recommend_models(
        use_case=use_case,
        top_k=top_k,
        private_required=(
            data_sensitivity == "High"
        )
    )

    trust_status = "Not Yet Validated"

    validation_strategy = build_validation_strategy(
        risk_level=risk["risk_level"],
        data_sensitivity=data_sensitivity,
        recommended_metrics=recommended_metrics
    )

    return {
        "use_case": use_case,
        "use_case_confidence": analysis[
            "confidence"
        ],
        "use_case_reason": analysis[
            "reason"
        ],
        "risk_level": risk[
            "risk_level"
        ],
        "risk_reason": risk[
            "reason"
        ],
        "data_sensitivity": data_sensitivity,
        "recommended_dataset": recommended_dataset,
        "recommended_config": recommended_dataset,
        "recommended_metrics": recommended_metrics,
        "recommended_models": model_recommendations[
            "recommendations"
        ],
        "validation_strategy": validation_strategy,
        "trust_status": trust_status
    }
# =========================================================
# VALIDATION STRATEGY
# =========================================================

def build_validation_strategy(
    risk_level,
    data_sensitivity,
    recommended_metrics
):

    strategy = []

    strategy.append(
        "Run benchmark before production deployment."
    )

    strategy.append(
        "Evaluate recommended models using DRS."
    )

    strategy.append(
        "Generate executive and sample-level reports."
    )

    if "factuality" in recommended_metrics:

        strategy.append(
            "Prioritize factuality validation."
        )

    if "hallucination" in recommended_metrics:

        strategy.append(
            "Enable hallucination probability analysis."
        )

    if "safety" in recommended_metrics:

        strategy.append(
            "Run safety and unsafe-output checks."
        )

    if risk_level == "High":

        strategy.append(
            "Require human review before deployment."
        )

    if data_sensitivity == "High":

        strategy.append(
            "Prefer private or on-prem deployment."
        )

    return strategy
from openvals.advisor.profiles import (
    list_use_cases
)


# =========================================================
# KEYWORD MAP
# =========================================================

USE_CASE_KEYWORDS = {
    "finance": [
        "finance",
        "bank",
        "banking",
        "investment",
        "loan",
        "credit",
        "insurance",
        "trading",
        "portfolio",
        "risk",
        "fraud"
    ],

    "cybersecurity": [
        "cybersecurity",
        "security",
        "soc",
        "siem",
        "xdr",
        "threat",
        "vulnerability",
        "phishing",
        "malware",
        "incident",
        "attack"
    ],

    "legal": [
        "legal",
        "law",
        "contract",
        "compliance",
        "policy",
        "regulation",
        "agreement",
        "clause",
        "audit"
    ],

    "coding": [
        "code",
        "coding",
        "developer",
        "software",
        "debug",
        "programming",
        "repository",
        "api",
        "sdk",
        "github"
    ],

    "customer_support": [
        "customer support",
        "support",
        "chatbot",
        "helpdesk",
        "ticket",
        "service desk",
        "customer service",
        "faq"
    ],

    "reasoning": [
        "reasoning",
        "analysis",
        "planning",
        "decision",
        "strategy",
        "multi-step",
        "complex",
        "research"
    ],

    "enterprise_ops": [
        "enterprise",
        "operations",
        "workflow",
        "hr",
        "crm",
        "itms",
        "itsm",
        "knowledge base",
        "automation",
        "process"
    ],

    "private_ai": [
        "private ai",
        "on-prem",
        "on premises",
        "local",
        "data privacy",
        "data residency",
        "confidential",
        "sensitive data",
        "internal network"
    ]
}


# =========================================================
# ANALYZE USE CASE TEXT
# =========================================================

def analyze_use_case_text(text):

    if not text:

        return {
            "use_case": "enterprise_ops",
            "confidence": 0.0,
            "scores": {},
            "reason": "No text provided; defaulted to enterprise_ops."
        }

    normalized = text.lower()

    scores = {}

    for use_case, keywords in USE_CASE_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in normalized:
                score += 1

        scores[use_case] = score

    best_use_case = max(
        scores,
        key=scores.get
    )

    best_score = scores[
        best_use_case
    ]

    total_matches = sum(
        scores.values()
    )

    if best_score == 0:

        return {
            "use_case": "enterprise_ops",
            "confidence": 0.25,
            "scores": scores,
            "reason": (
                "No strong domain match found; "
                "defaulted to enterprise_ops."
            )
        }

    confidence = best_score / max(
        total_matches,
        1
    )

    confidence = round(
        confidence,
        3
    )

    return {
        "use_case": best_use_case,
        "confidence": confidence,
        "scores": scores,
        "reason": (
            f"Matched use case '{best_use_case}' "
            f"based on {best_score} keyword signals."
        )
    }


# =========================================================
# VALIDATE USE CASE
# =========================================================

def is_known_use_case(use_case):

    return use_case in list_use_cases()
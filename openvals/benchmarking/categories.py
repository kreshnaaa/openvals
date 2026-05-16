# =========================================================
# OPENVALS BENCHMARK CATEGORIES
# =========================================================

BENCHMARK_CATEGORIES = {

    "reasoning": {
        "weight": 1.0,
        "description": "Logical reasoning and decision making"
    },

    "coding": {
        "weight": 1.1,
        "description": "Code generation and debugging"
    },

    "cybersecurity": {
        "weight": 1.3,
        "description": "Security analysis and threat detection"
    },

    "math": {
        "weight": 1.0,
        "description": "Mathematical reasoning and calculations"
    },

    "legal": {
        "weight": 1.2,
        "description": "Legal interpretation and compliance"
    },

    "enterprise_ops": {
        "weight": 1.1,
        "description": "Enterprise workflow and operational tasks"
    }

}


# =========================================================
# CATEGORY SCORING
# =========================================================

def calculate_category_score(metrics, category):

    base_score = (
        metrics.get("accuracy", 0) * 0.30 +
        metrics.get("semantic", 0) * 0.20 +
        metrics.get("reliability", 0) * 0.20 +
        metrics.get("safety", 0) * 0.15 +
        metrics.get("consistency", 0) * 0.15
    )

    category_weight = BENCHMARK_CATEGORIES.get(
        category,
        {}
    ).get("weight", 1.0)

    return round(base_score * category_weight, 3)


# =========================================================
# GENERATE CATEGORY RESULTS
# =========================================================

def evaluate_categories(results):

    category_results = {}

    for model, data in results.items():

        metrics = data["metrics"]

        model_scores = {}

        for category in BENCHMARK_CATEGORIES:

            score = calculate_category_score(
                metrics,
                category
            )

            model_scores[category] = score

        category_results[model] = model_scores

    return category_results
import subprocess


# =========================================================
# STATIC MODEL INTELLIGENCE
# Known model profiles
# =========================================================

STATIC_MODEL_CATALOG = {
    "llama3": {
        "provider": "ollama",
        "model_type": "local",
        "private_ready": True,
        "enterprise_ready": True,
        "strengths": [
            "general reasoning",
            "chat",
            "summarization",
            "private deployment"
        ],
        "capabilities": {
            "reasoning": 0.82,
            "coding": 0.70,
            "math": 0.68,
            "finance": 0.72,
            "cybersecurity": 0.70,
            "legal": 0.65,
            "customer_support": 0.82,
            "latency": 0.72,
            "cost_efficiency": 0.90,
            "privacy": 0.95,
            "safety": 0.78
        }
    },

    "mistral": {
        "provider": "ollama",
        "model_type": "local",
        "private_ready": True,
        "enterprise_ready": True,
        "strengths": [
            "speed",
            "general reasoning",
            "cost efficiency",
            "local deployment"
        ],
        "capabilities": {
            "reasoning": 0.78,
            "coding": 0.72,
            "math": 0.66,
            "finance": 0.70,
            "cybersecurity": 0.72,
            "legal": 0.63,
            "customer_support": 0.78,
            "latency": 0.86,
            "cost_efficiency": 0.92,
            "privacy": 0.95,
            "safety": 0.76
        }
    },

    "llama2": {
        "provider": "ollama",
        "model_type": "local",
        "private_ready": True,
        "enterprise_ready": False,
        "strengths": [
            "lightweight",
            "simple tasks",
            "local experimentation"
        ],
        "capabilities": {
            "reasoning": 0.62,
            "coding": 0.55,
            "math": 0.52,
            "finance": 0.55,
            "cybersecurity": 0.56,
            "legal": 0.50,
            "customer_support": 0.62,
            "latency": 0.82,
            "cost_efficiency": 0.94,
            "privacy": 0.95,
            "safety": 0.68
        }
    },

    "deepseek-r1:8b": {
        "provider": "ollama",
        "model_type": "local",
        "private_ready": True,
        "enterprise_ready": True,
        "strengths": [
            "reasoning",
            "math",
            "technical problem solving",
            "private deployment"
        ],
        "capabilities": {
            "reasoning": 0.88,
            "coding": 0.78,
            "math": 0.84,
            "finance": 0.74,
            "cybersecurity": 0.76,
            "legal": 0.62,
            "customer_support": 0.70,
            "latency": 0.62,
            "cost_efficiency": 0.86,
            "privacy": 0.95,
            "safety": 0.72
        }
    }
}


# =========================================================
# DISCOVER INSTALLED OLLAMA MODELS
# =========================================================

def discover_ollama_models():

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        models = []

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line or line.lower().startswith("name"):
                continue

            model_name = line.split()[0]

            models.append(
                model_name
            )

        return models

    except Exception:
        return []


# =========================================================
# NORMALIZE MODEL NAME
# =========================================================

def normalize_model_name(model_name):

    if model_name.endswith(":latest"):

        return model_name.replace(
            ":latest",
            ""
        )

    return model_name


# =========================================================
# GENERIC PROFILE FOR UNKNOWN MODELS
# =========================================================

def build_generic_profile(model_name):

    normalized = normalize_model_name(
        model_name
    ).lower()

    capabilities = {
        "reasoning": 0.65,
        "coding": 0.60,
        "math": 0.60,
        "finance": 0.60,
        "cybersecurity": 0.60,
        "legal": 0.55,
        "customer_support": 0.65,
        "latency": 0.70,
        "cost_efficiency": 0.80,
        "privacy": 0.95,
        "safety": 0.65
    }

    strengths = [
        "local deployment",
        "private AI",
        "general purpose evaluation"
    ]

    enterprise_ready = True

    if "qwen" in normalized:
        capabilities.update({
            "reasoning": 0.78,
            "coding": 0.76,
            "math": 0.78,
            "customer_support": 0.72
        })

        strengths = [
            "reasoning",
            "coding",
            "math",
            "local deployment"
        ]

    elif "gpt-oss" in normalized:
        capabilities.update({
            "reasoning": 0.84,
            "coding": 0.78,
            "finance": 0.76,
            "customer_support": 0.80,
            "safety": 0.76,
            "latency": 0.58
        })

        strengths = [
            "reasoning",
            "enterprise analysis",
            "private deployment",
            "general intelligence"
        ]

    elif "gemma" in normalized:
        capabilities.update({
            "reasoning": 0.72,
            "customer_support": 0.74,
            "latency": 0.78,
            "cost_efficiency": 0.86
        })

        strengths = [
            "lightweight",
            "chat",
            "fast local inference"
        ]

    elif "phi" in normalized:
        capabilities.update({
            "reasoning": 0.70,
            "coding": 0.72,
            "latency": 0.84,
            "cost_efficiency": 0.90
        })

        strengths = [
            "small model",
            "coding",
            "fast inference"
        ]

    elif "deepseek" in normalized:
        capabilities.update({
            "reasoning": 0.86,
            "coding": 0.80,
            "math": 0.84,
            "latency": 0.62
        })

        strengths = [
            "reasoning",
            "math",
            "technical problem solving"
        ]

    return {
        "provider": "ollama",
        "model_type": "local",
        "private_ready": True,
        "enterprise_ready": enterprise_ready,
        "dynamic": True,
        "strengths": strengths,
        "capabilities": capabilities
    }


# =========================================================
# BUILD DYNAMIC CATALOG
# =========================================================

def get_model_catalog(
    installed_only=True
):

    catalog = {}

    installed_models = discover_ollama_models()

    if installed_only:

        for model_name in installed_models:

            normalized = normalize_model_name(
                model_name
            )

            if normalized in STATIC_MODEL_CATALOG:

                catalog[model_name] = STATIC_MODEL_CATALOG[
                    normalized
                ]

            elif model_name in STATIC_MODEL_CATALOG:

                catalog[model_name] = STATIC_MODEL_CATALOG[
                    model_name
                ]

            else:

                catalog[model_name] = build_generic_profile(
                    model_name
                )

        return catalog

    return {
        **STATIC_MODEL_CATALOG
    }


# =========================================================
# PROFILE LOOKUP
# =========================================================

def get_model_profile(model_name):

    catalog = get_model_catalog(
        installed_only=True
    )

    if model_name in catalog:
        return catalog[model_name]

    normalized = normalize_model_name(
        model_name
    )

    if normalized in STATIC_MODEL_CATALOG:
        return STATIC_MODEL_CATALOG[
            normalized
        ]

    return build_generic_profile(
        model_name
    )


# =========================================================
# LIST MODELS
# =========================================================

def list_models(
    installed_only=True
):

    return list(
        get_model_catalog(
            installed_only=installed_only
        ).keys()
    )
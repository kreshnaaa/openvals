MODEL_CATALOG = {
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


def get_model_catalog():
    return MODEL_CATALOG


def get_model_profile(model_name):
    return MODEL_CATALOG.get(model_name)


def list_models():
    return list(MODEL_CATALOG.keys())
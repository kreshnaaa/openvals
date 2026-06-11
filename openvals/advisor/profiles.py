USE_CASE_PROFILES = {
    "customer_support": {
        "description": "Customer support chatbot or service assistant",
        "weights": {
            "customer_support": 0.25,
            "safety": 0.25,
            "latency": 0.20,
            "cost_efficiency": 0.15,
            "privacy": 0.15
        }
    },

    "finance": {
        "description": "Finance, investment, banking, or financial advisory use case",
        "weights": {
            "finance": 0.30,
            "reasoning": 0.20,
            "safety": 0.20,
            "privacy": 0.20,
            "latency": 0.10
        }
    },

    "cybersecurity": {
        "description": "Security analysis, SOC assistant, risk detection, or cyber advisory",
        "weights": {
            "cybersecurity": 0.30,
            "reasoning": 0.20,
            "safety": 0.20,
            "privacy": 0.20,
            "latency": 0.10
        }
    },

    "legal": {
        "description": "Legal review, contract analysis, or compliance support",
        "weights": {
            "legal": 0.30,
            "reasoning": 0.25,
            "safety": 0.20,
            "privacy": 0.20,
            "latency": 0.05
        }
    },

    "coding": {
        "description": "Code generation, code review, debugging, or developer assistant",
        "weights": {
            "coding": 0.40,
            "reasoning": 0.25,
            "math": 0.10,
            "latency": 0.15,
            "cost_efficiency": 0.10
        }
    },

    "reasoning": {
        "description": "Complex reasoning, analysis, planning, or multi-step problem solving",
        "weights": {
            "reasoning": 0.45,
            "math": 0.20,
            "safety": 0.15,
            "privacy": 0.10,
            "latency": 0.10
        }
    },

    "enterprise_ops": {
        "description": "Enterprise operations, internal automation, knowledge work, and workflows",
        "weights": {
            "reasoning": 0.25,
            "customer_support": 0.20,
            "privacy": 0.20,
            "safety": 0.15,
            "latency": 0.10,
            "cost_efficiency": 0.10
        }
    },

    "private_ai": {
        "description": "Private AI deployment where data ownership and control are critical",
        "weights": {
            "privacy": 0.35,
            "safety": 0.20,
            "reasoning": 0.20,
            "cost_efficiency": 0.15,
            "latency": 0.10
        }
    }
}


def get_use_case_profiles():
    return USE_CASE_PROFILES


def get_use_case_profile(use_case):
    return USE_CASE_PROFILES.get(use_case)


def list_use_cases():
    return list(USE_CASE_PROFILES.keys())
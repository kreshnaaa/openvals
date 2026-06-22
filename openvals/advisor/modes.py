MODES = {

    "quick": {
        "top_k": 2,
        "sample_limit": 3,
        "max_workers": 2,
        "description": "Fast trust assessment"
    },

    "standard": {
        "top_k": 3,
        "sample_limit": 10,
        "max_workers": 8,
        "description": "Balanced evaluation"
    },

    "full": {
        "top_k": None,
        "sample_limit": None,
        "max_workers": None,
        "description": "Complete benchmark"
    }
}
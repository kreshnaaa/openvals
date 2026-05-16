REASONING_BENCHMARKS = [

    {
        "id": "reasoning_001",

        "question": """
        If a server crashes during a database migration,
        what should be done first?
        """,

        "expected_keywords": [
            "rollback",
            "backup",
            "recovery",
            "integrity"
        ],

        "difficulty": "medium"
    },

    {
        "id": "reasoning_002",

        "question": """
        A company detects unusual login activity from
        multiple countries simultaneously. What does this indicate?
        """,

        "expected_keywords": [
            "credential compromise",
            "account takeover",
            "incident response"
        ],

        "difficulty": "high"
    }
]
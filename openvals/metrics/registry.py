from openvals.metrics.performance.accuracy import accuracy
from openvals.metrics.performance.semantic import semantic_similarity
from openvals.metrics.performance.latency import measure_latency

from openvals.metrics.trust.reliability import reliability_score
from openvals.metrics.trust.safety import safety
from openvals.metrics.trust.consistency import consistency
from openvals.metrics.trust.variance import variance
from openvals.metrics.trust.hallucination import hallucination_analysis

METRIC_REGISTRY = {

    # =====================================================
    # PERFORMANCE METRICS
    # =====================================================

    "accuracy": {

        "category": "performance",

        "direction": "higher",

        "weightable": True,

        "description":
            "Measures exact correctness of output"

    },

    "semantic": {

        "category": "performance",

        "direction": "higher",

        "weightable": True,

        "description":
            "Embedding-based semantic similarity"

    },

    "latency": {

        "category": "performance",

        "direction": "lower",

        "weightable": True,

        "description":
            "Inference response time"

    },


    # =====================================================
    # TRUST METRICS
    # =====================================================

    "reliability": {

        "category": "trust",

        "direction": "higher",

        "weightable": True,

        "description":
            "Stability across evaluations"

    },

    "safety": {

        "category": "trust",

        "direction": "higher",

        "weightable": True,

        "description":
            "Measures harmful or unsafe behavior"

    },

    "consistency": {

        "category": "trust",

        "direction": "higher",

        "weightable": True,

        "description":
            "Repeatability of outputs"

    },

    "variance": {

        "category": "trust",

        "direction": "lower",

        "weightable": True,

        "description":
            "Output fluctuation measurement"

    },

    "hallucination": {

        "category": "trust",

        "direction": "lower",

        "weightable": True,

        "description":
            "Probability of fabricated information"

    },


    # =====================================================
    # INFRASTRUCTURE METRICS
    # =====================================================

    "compute": {

        "category": "infrastructure",

        "direction": "lower",

        "weightable": False,

        "description":
            "Compute resource usage"

    },

    "energy": {

        "category": "infrastructure",

        "direction": "lower",

        "weightable": False,

        "description":
            "Energy consumption"

    },

    "carbon": {

        "category": "infrastructure",

        "direction": "lower",

        "weightable": False,

        "description":
            "Estimated carbon footprint"

    }

}
from openvals.metrics.performance.accuracy import accuracy
from openvals.metrics.performance.semantic import semantic_similarity
from openvals.metrics.performance.latency import measure_latency

from openvals.metrics.trust.reliability import reliability_score
from openvals.metrics.trust.safety import safety
from openvals.metrics.trust.consistency import consistency
from openvals.metrics.trust.variance import variance
from openvals.metrics.trust.hallucination import hallucination_analysis
from openvals.metrics.trust.factuality import factuality_score

from openvals.scoring.weighted import weighted_score
from openvals.scoring.drs import compute_drs

from openvals.metrics.registry import METRIC_REGISTRY
# =====================================================
# PERFORMANCE
# =====================================================

def run_accuracy(output, expected, config):

    return accuracy(
        output,
        expected,
        config
    )

def run_semantic(output, expected):

    return semantic_similarity(
        output,
        expected
    )

def run_latency(fn, prompt):

    return measure_latency(
        fn,
        prompt
    )

# =====================================================
# TRUST
# =====================================================

def run_reliability(model, prompt):

    return reliability_score(
        model,
        prompt
    )

def run_safety(output):

    return safety(output)

def run_consistency(model, prompt):

    return consistency(
        model,
        prompt
    )

def run_variance(outputs):

    return variance(outputs)

def run_hallucination(output_text, metrics):

    return hallucination_analysis(
        output_text=output_text,
        metrics=metrics
    )

def run_factuality(output, expected):

    return factuality_score(
        output_text=output,
        expected_text=expected
    )
    return result
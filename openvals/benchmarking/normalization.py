import math
import statistics

# =========================================================
# METRICS
# =========================================================

METRICS = [

    "accuracy",
    "semantic",
    "latency",
    "reliability",
    "safety",
    "consistency",
    "variance",
    "hallucination",
    "factuality"

]

# =========================================================
# INVERSE METRICS
# LOWER IS BETTER
# =========================================================

INVERSE_METRICS = [

    "latency",
    "variance",
    "hallucination"

]

# =========================================================
# CLIP
# =========================================================

def clip(

    value,
    min_value=0.0,
    max_value=1.0

):

    return max(

        min(value, max_value),
        min_value

    )


# =========================================================
# SAFE VALUE
# =========================================================

def safe_metric(value):

    if value is None:
        return 0.0

    if isinstance(value, (int, float)):

        if math.isnan(value):
            return 0.0

        if math.isinf(value):
            return 0.0

        return float(value)

    return 0.0


# =========================================================
# PERCENTILE RANK
# =========================================================

def percentile_rank(

    value,
    values

):

    sorted_vals = sorted(values)

    count = len(sorted_vals)

    if count <= 1:
        return 1.0

    below = len(

        [
            v for v in sorted_vals
            if v <= value
        ]

    )

    return (

        (below - 1)
        /
        (count - 1)

    )


# =========================================================
# LOG TRANSFORM
# =========================================================

def transform_metric(

    metric,
    value

):

    # ==============================================
    # LATENCY
    # ==============================================

    if metric == "latency":

        return math.log(value + 1)

    # ==============================================
    # HALLUCINATION
    # ==============================================

    elif metric == "hallucination":

        return value

    return value


# =========================================================
# NORMALIZATION ENGINE
# =========================================================

def normalize_scores(

    results,
    method="hybrid"

):

    """
    Supported Methods:

    - minmax
    - zscore
    - percentile
    - hybrid
    """

    # =====================================================
    # COLLECT METRICS
    # =====================================================

    values = {

        metric: []

        for metric in METRICS

    }

    for model_name in results:

        metrics = results[model_name]["metrics"]

        for metric in METRICS:

            value = safe_metric(

                metrics.get(metric, 0.0)

            )

            value = transform_metric(
                metric,
                value
            )

            values[metric].append(value)

    # =====================================================
    # COMPUTE STATS
    # =====================================================

    min_vals = {

        metric: min(values[metric])

        for metric in METRICS

    }

    max_vals = {

        metric: max(values[metric])

        for metric in METRICS

    }

    means = {

        metric: statistics.mean(
            values[metric]
        )

        for metric in METRICS

    }

    stds = {}

    for metric in METRICS:

        try:

            stds[metric] = statistics.stdev(
                values[metric]
            )

        except:

            stds[metric] = 0.0

    # =====================================================
    # NORMALIZATION
    # =====================================================

    normalized = {}

    for model_name in results:

        normalized[model_name] = {}

        metrics = results[model_name]["metrics"]

        for metric in METRICS:

            raw_value = safe_metric(

                metrics.get(metric, 0.0)

            )

            value = transform_metric(
                metric,
                raw_value
            )

            min_v = min_vals[metric]
            max_v = max_vals[metric]

            mean_v = means[metric]
            std_v = stds[metric]

            # ==============================================
            # IDENTICAL VALUES
            # ==============================================

            if max_v == min_v:

                norm = 1.0

            else:

                # ==========================================
                # MINMAX
                # ==========================================

                if method == "minmax":

                    norm = (

                        (value - min_v)

                        /

                        (max_v - min_v)

                    )

                # ==========================================
                # ZSCORE
                # ==========================================

                elif method == "zscore":

                    if std_v == 0:

                        norm = 1.0

                    else:

                        z = (

                            (value - mean_v)

                            /

                            std_v

                        )

                        norm = (

                            0.5
                            +
                            (z / 6)

                        )

                # ==========================================
                # PERCENTILE
                # ==========================================

                elif method == "percentile":

                    norm = percentile_rank(

                        value,
                        values[metric]

                    )

                # ==========================================
                # HYBRID
                # ==========================================

                else:

                    minmax = (

                        (value - min_v)

                        /

                        (max_v - min_v)

                    )

                    percentile = percentile_rank(

                        value,
                        values[metric]

                    )

                    norm = (

                        (minmax * 0.7)

                        +

                        (percentile * 0.3)

                    )

                # ==========================================
                # INVERSE METRICS
                # ==========================================

                if metric in INVERSE_METRICS:

                    norm = 1 - norm

            normalized[model_name][metric] = round(

                clip(norm),
                4

            )

    return normalized
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
    "variance"

]


# =========================================================
# CLIP
# =========================================================

def clip(value, min_value=0.0, max_value=1.0):

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

def percentile_rank(value, values):

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

    return (below - 1) / (count - 1)


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

    values = {
        metric: []
        for metric in METRICS
    }


    # =====================================================
    # COLLECT METRICS
    # =====================================================

    for model_name in results:

        metrics = results[model_name]["metrics"]

        for metric in METRICS:

            value = safe_metric(
                metrics.get(metric, 0.0)
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
        metric: statistics.mean(values[metric])
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


    normalized = {}


    # =====================================================
    # NORMALIZE MODELS
    # =====================================================

    for model_name in results:

        normalized[model_name] = {}

        metrics = results[model_name]["metrics"]


        for metric in METRICS:

            value = safe_metric(
                metrics.get(metric, 0.0)
            )

            min_v = min_vals[metric]
            max_v = max_vals[metric]

            mean_v = means[metric]
            std_v = stds[metric]


            # ==============================================
            # HANDLE IDENTICAL VALUES
            # ==============================================

            if max_v == min_v:

                norm = 1.0


            else:

                # ==========================================
                # LATENCY TRANSFORMATION
                # ==========================================

                if metric == "latency":

                    value = math.log(value + 1)

                    min_v = math.log(min_v + 1)
                    max_v = math.log(max_v + 1)


                # ==========================================
                # METHOD: MINMAX
                # ==========================================

                if method == "minmax":

                    norm = (
                        (value - min_v)
                        /
                        (max_v - min_v)
                    )


                # ==========================================
                # METHOD: Z-SCORE
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
                            0.5 +
                            (z / 6)
                        )


                # ==========================================
                # METHOD: PERCENTILE
                # ==========================================

                elif method == "percentile":

                    norm = percentile_rank(
                        value,
                        values[metric]
                    )


                # ==========================================
                # METHOD: HYBRID
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
                # LOWER IS BETTER
                # ==========================================

                if metric in [

                    "latency",
                    "variance"

                ]:

                    norm = 1 - norm


            normalized[model_name][metric] = round(
                clip(norm),
                4
            )


    return normalized
from openvals.core.evaluator_helpers import (

    run_accuracy,
    run_factuality,
    run_semantic,
    run_reliability,
    run_safety,
    run_consistency,
    run_variance,
    run_hallucination,
    run_latency
)

from openvals.scoring.weighted import weighted_score
from openvals.scoring.drs import compute_drs


class Evaluator:

    def __init__(

        self,
        model,
        dataset,
        weights=None,
        debug=False

    ):

        self.model = model
        self.dataset = dataset
        self.debug = debug

        self.weights = weights or {

            "accuracy": 0.25,
            "semantic": 0.15,
            "safety": 0.15,
            "hallucination": 0.15,
            "factuality": 0.20,
            "reliability": 0.10,
            "latency": 0.05

        }

    # =====================================================
    # RUN EVALUATION
    # =====================================================

    def run(self):

        results = []

        agg = {

            "accuracy": 0.0,
            "semantic": 0.0,
            "latency": 0.0,
            "reliability": 0.0,
            "safety": 0.0,
            "consistency": 0.0,
            "variance": 0.0,
            "hallucination": 0.0,
            "factuality": 0.0

        }

        # =================================================
        # PROCESS DATASET
        # =================================================

        for sample in self.dataset:

            # =============================================
            # BACKWARD COMPATIBILITY
            # =============================================

            prompt = sample.get(

                "prompt",
                sample.get("input", "")

            )

            expected = sample.get(
                "expected_output",
                ""
            )

            eval_config = sample.get(
                "evaluation",
                {}
            )

            task_type = sample.get(
                "type",
                "default"
            )

            try:

                # =========================================
                # GENERATE OUTPUT + LATENCY
                # =========================================

                output, latency = run_latency(

                    self.model.generate,
                    prompt

                )

                if output is None:
                    output = ""

                # =========================================
                # HANDLE MODEL FAILURES
                # =========================================

                if (

                    isinstance(output, str)

                    and output.startswith("ERROR")

                ):

                    raise Exception(output)

                # =========================================
                # PERFORMANCE METRICS
                # =========================================

                acc = run_accuracy(

                    output,
                    expected,
                    eval_config

                )

                sem = run_semantic(
                    output,
                    expected
                )

                threshold = eval_config.get(
                    "semantic_threshold"
                )

                if (

                    threshold is not None

                    and sem >= threshold

                ):

                    sem = 1.0

                # =========================================
                # TASK-AWARE LOGIC
                # =========================================

                if task_type == "classification":

                    sem = acc

                elif task_type == "generation":

                    if len(output.split()) > 120:

                        sem *= 0.9

                # =========================================
                # TRUST METRICS
                # =========================================

                rel = run_reliability(

                    self.model,
                    prompt

                )

                saf = run_safety(output)

                cons = run_consistency(

                    self.model,
                    prompt

                )

                var = run_variance([output])

                # =========================================
                # HPI / HALLUCINATION
                # =========================================

                metrics_snapshot = {

                    "semantic": sem,
                    "consistency": cons,
                    "variance": var

                }

                hpi_result = run_hallucination(

                    output,
                    metrics_snapshot

                )

                hall = hpi_result[
                    "hpi_score"
                ]
                # =========================================
                # FACTUALITY
                # =========================================
                factual_result = run_factuality(
                    output,
                    expected
                )
                factuality = factual_result["factuality_score"]

            except Exception as e:

                output = f"ERROR: {str(e)}"

                latency = 0.0
                acc = 0.0
                sem = 0.0
                rel = 0.0
                saf = 0.0
                cons = 0.0
                var = 0.0
                hall = 0.0
                factuality = 0.0
                factual_result = {
                    "factual_score": 0.0,
                    "risk_level": "Critical",
                }
                hpi_result = {

                    "hpi_score": 1.0,
                    "risk_level": "Critical",
                    "overconfidence_matches": []

                }

            # =============================================
            # DEBUG LOGGING
            # =============================================

            if self.debug:

                print("\n-----------------------------")

                print(f"Prompt: {prompt}")

                print(f"Output: {output}")

                print(f"Accuracy: {acc:.3f}")

                print(f"Semantic: {sem:.3f}")

                print(f"Latency: {latency:.2f} ms")

                print(f"Reliability: {rel:.3f}")

                print(f"Safety: {saf:.3f}")

                print(f"Consistency: {cons:.3f}")

                print(f"Variance: {var:.3f}")

                print(f"Hallucination: {hall:.3f}")

                print(
                    f"HPI Risk: "
                    f"{hpi_result['risk_level']}"
                )
                print(f"Factuality: {factuality:.3f}")

            # =============================================
            # AGGREGATION
            # =============================================

            agg["accuracy"] += acc
            agg["semantic"] += sem
            agg["latency"] += latency
            agg["reliability"] += rel
            agg["safety"] += saf
            agg["consistency"] += cons
            agg["variance"] += var
            agg["hallucination"] += hall
            agg["factuality"] += factuality

            # =============================================
            # STORE SAMPLE RESULT
            # =============================================

            results.append({

                "prompt": prompt,

                "output": output,

                "expected": expected,

                "accuracy": round(acc, 3),

                "semantic": round(sem, 3),

                "latency": round(latency, 2),

                "reliability": round(rel, 3),

                "safety": round(saf, 3),

                "consistency": round(cons, 3),

                "variance": round(var, 3),

                "hallucination": round(hall, 3),
                "hallucination_analysis": hpi_result,   
                "factuality": round(factuality, 3),
                "factual_analysis": factual_result
                

            })

        # =================================================
        # FINAL AGGREGATION
        # =================================================

        n = len(self.dataset) if self.dataset else 1

        avg_metrics = {

            k: v / n

            for k, v in agg.items()

        }

        # =================================================
        # FINAL SCORING
        # =================================================

        score = weighted_score(

            avg_metrics,
            self.weights

        )

        drs_score = compute_drs(
            avg_metrics
        )

        # =================================================
        # RETURN RESULTS
        # =================================================

        return {

            "overall_score": round(
                score,
                3
            ),

            "drs_score": round(
                drs_score,
                3
            ),

            "metrics": {

                k: round(v, 3)

                for k, v in avg_metrics.items()

            },

            "samples": results

        }
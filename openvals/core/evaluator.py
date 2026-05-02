from openvals.metrics.accuracy import accuracy
from openvals.metrics.semantic import semantic_similarity
from openvals.metrics.latency import measure_latency
from openvals.scoring.weighted import weighted_score


class Evaluator:
    def __init__(self, model, dataset, weights=None, debug=False):
        self.model = model
        self.dataset = dataset
        self.weights = weights or {
            "accuracy": 0.4,
            "semantic": 0.4,
            "latency": 0.2
        }
        self.debug = debug

    def run(self):
        results = []

        agg = {
            "accuracy": 0.0,
            "semantic": 0.0,
            "latency": 0.0
        }

        for sample in self.dataset:
            try:
                output, latency = measure_latency(
                    self.model.generate,
                    sample["input"]
                )

                acc = accuracy(output, sample["expected_output"])
                sem = semantic_similarity(output, sample["expected_output"])

            except Exception as e:
                output = f"ERROR: {str(e)}"
                latency = 0.0
                acc = 0.0
                sem = 0.0

            # ✅ Debug block (toggle with debug=True)
            if self.debug:
                print("\n-----------------------------")
                print(f"Input: {sample['input']}")
                print(f"Expected: {sample['expected_output']}")
                print(f"Output: {output}")
                print(f"Accuracy: {acc:.3f}")
                print(f"Semantic: {sem:.3f}")
                print(f"Latency: {latency:.2f} ms")

            agg["accuracy"] += acc
            agg["semantic"] += sem
            agg["latency"] += latency

            results.append({
                "input": sample["input"],
                "output": output,
                "expected": sample["expected_output"],
                "accuracy": round(acc, 3),
                "semantic": round(sem, 3),
                "latency": round(latency, 2)
            })

        n = len(self.dataset) if self.dataset else 1

        avg_metrics = {
            "accuracy": agg["accuracy"] / n,
            "semantic": agg["semantic"] / n,
            "latency": agg["latency"] / n
        }

        score = weighted_score(avg_metrics, self.weights)

        return {
            "overall_score": round(score, 3),
            "metrics": {
                "accuracy": round(avg_metrics["accuracy"], 3),
                "semantic": round(avg_metrics["semantic"], 3),
                "latency": round(avg_metrics["latency"], 2)
            },
            "samples": results
        }
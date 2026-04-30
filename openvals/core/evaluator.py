
from openvals.metrics.accuracy import accuracy
from openvals.metrics.semantic import semantic_similarity
from openvals.metrics.latency import measure_latency
from openvals.scoring.weighted import weighted_score

class Evaluator:
    def __init__(self, model, dataset, weights=None):
        self.model = model
        self.dataset = dataset
        self.weights = weights or {"accuracy": 0.4, "semantic": 0.4, "latency": 0.2}

    def run(self):
        results = []
        agg = {"accuracy": 0, "semantic": 0, "latency": 0}

        for sample in self.dataset:
            output, latency = measure_latency(self.model.generate, sample["input"])
            acc = accuracy(output, sample["expected_output"])
            sem = semantic_similarity(output, sample["expected_output"])

            agg["accuracy"] += acc
            agg["semantic"] += sem
            agg["latency"] += latency

            results.append({
                "input": sample["input"],
                "output": output,
                "expected": sample["expected_output"],
                "accuracy": acc,
                "semantic": sem,
                "latency": latency
            })

        n = len(self.dataset)
        avg_metrics = {k: v/n for k, v in agg.items()}
        score = weighted_score(avg_metrics, self.weights)

        return {
            "overall_score": score,
            "metrics": avg_metrics,
            "samples": results
        }

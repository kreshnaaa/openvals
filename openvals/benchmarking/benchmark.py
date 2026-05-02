from openvals.core.evaluator import Evaluator

class BenchmarkRunner:
    def __init__(self, models, dataset, weights=None, debug=False):
        self.models = models
        self.dataset = dataset
        self.weights = weights
        self.debug = debug

    def run(self):
        results = {}

        for name, model in self.models.items():
            print(f"\n🚀 Running model: {name}")

            try:
                evaluator = Evaluator(
                    model=model,
                    dataset=self.dataset,
                    weights=self.weights,
                    debug=self.debug
                )

                result = evaluator.run()

                # ✅ CRITICAL SAFETY CHECK
                if result is None:
                    print(f"❌ ERROR: {name} returned None")
                    results[name] = self._empty_result()
                    continue

                # ✅ DEBUG PRINT
                if self.debug:
                    print("DEBUG RESULT:", result)

                results[name] = result

            except Exception as e:
                print(f"🔥 CRITICAL ERROR in model {name}: {str(e)}")
                results[name] = self._empty_result()

        return results

    def _empty_result(self):
        return {
            "overall_score": 0.0,
            "metrics": {
                "accuracy": 0.0,
                "semantic": 0.0,
                "latency": 0.0,
                "reliability": 0.0,
                "safety": 0.0
            },
            "samples": []
        }
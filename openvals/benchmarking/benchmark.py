from concurrent.futures import ThreadPoolExecutor, as_completed

from openvals.core.evaluator import Evaluator


class BenchmarkRunner:

    def __init__(
        self,
        models,
        dataset,
        weights=None,
        debug=False,
        parallel=False,
        max_workers=3
    ):
        self.models = models
        self.dataset = dataset
        self.weights = weights
        self.debug = debug
        self.parallel = parallel
        self.max_workers = max_workers

    def run(self):
        if self.parallel:
            return self._run_parallel()

        return self._run_sequential()

    def _run_sequential(self):
        results = {}

        for name, model in self.models.items():
            results[name] = self._run_single_model(
                name,
                model
            )

        return results

    def _run_parallel(self):
        results = {}

        workers = min(
            self.max_workers,
            len(self.models)
        )

        with ThreadPoolExecutor(
            max_workers=workers
        ) as executor:

            futures = {
                executor.submit(
                    self._run_single_model,
                    name,
                    model
                ): name
                for name, model in self.models.items()
            }

            for future in as_completed(futures):
                name = futures[future]

                try:
                    results[name] = future.result()

                except Exception as e:
                    print(
                        f"🔥 CRITICAL ERROR in model "
                        f"{name}: {str(e)}"
                    )

                    results[name] = self._empty_result()

        return results

    def _run_single_model(self, name, model):
        print(f"\n🚀 Running model: {name}")

        try:
            evaluator = Evaluator(
                model=model,
                dataset=self.dataset,
                weights=self.weights,
                debug=self.debug
            )

            result = evaluator.run()

            if result is None:
                print(f"❌ ERROR: {name} returned None")
                return self._empty_result()

            if self.debug:
                print(f"DEBUG RESULT [{name}]:", result)

            return result

        except Exception as e:
            print(
                f"🔥 CRITICAL ERROR in model "
                f"{name}: {str(e)}"
            )

            return self._empty_result()

    def _empty_result(self):
        return {
            "overall_score": 0.0,
            "drs_score": 0.0,
            "metrics": {
                "accuracy": 0.0,
                "semantic": 0.0,
                "factuality": 0.0,
                "latency": 0.0,
                "reliability": 0.0,
                "safety": 0.0,
                "consistency": 0.0,
                "variance": 0.0,
                "hallucination": 1.0
            },
            "samples": []
        }

from concurrent.futures import ThreadPoolExecutor, as_completed
from openvals.core.evaluator import Evaluator


class BenchmarkRunner:
    def __init__(self, models, dataset, weights=None, parallel: bool = True):
        self.models = models
        self.dataset = dataset
        self.weights = weights
        self.parallel = parallel

    def _evaluate_model(self, name, model):
        """Run evaluation for a single model."""
        evaluator = Evaluator(model=model, dataset=self.dataset, weights=self.weights)
        return name, evaluator.run()

    def run(self):
        results = {}

        if self.parallel:
            # Run all models at the same time (faster)
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self._evaluate_model, name, model): name
                    for name, model in self.models.items()
                }
                for future in as_completed(futures):
                    name, result = future.result()
                    results[name] = result
        else:
            # Run models one by one (sequential)
            for name, model in self.models.items():
                _, result = self._evaluate_model(name, model)
                results[name] = result

        return results

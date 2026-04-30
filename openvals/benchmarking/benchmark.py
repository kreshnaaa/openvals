
from openvals.core.evaluator import Evaluator

class BenchmarkRunner:
    def __init__(self, models, dataset, weights=None):
        self.models = models
        self.dataset = dataset
        self.weights = weights

    def run(self):
        results = {}
        for name, model in self.models.items():
            evaluator = Evaluator(model=model, dataset=self.dataset, weights=self.weights)
            results[name] = evaluator.run()
        return results

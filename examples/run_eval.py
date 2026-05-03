from openvals.core.evaluator import Evaluator
from openvals.datasets.loader import load_dataset
from openvals.models.ollama_model import OllamaModel
dataset = load_dataset("examples/sample_eval.json")
model = OllamaModel("mistral")
evaluator = Evaluator(model, dataset)
result = evaluator.run()
print(result)
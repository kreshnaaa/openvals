from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.benchmarking.ranking import rank_models
from openvals.datasets.loader import load_dataset
from openvals.models.ollama_model import OllamaModel

dataset = load_dataset("examples/sample_eval.json")

models = {
    "llama2": OllamaModel("llama2"),
    "mistral": OllamaModel("mistral"),
    "llama3": OllamaModel("llama3")
}

runner = BenchmarkRunner(models, dataset)
results = runner.run()

normalized = normalize_scores(results)

ranking = rank_models(normalized, {
    "accuracy": 0.5,
    "latency": 0.5
})

# ✅ Pretty Table Output
print("\n=== Benchmark Results ===\n")
print(f"{'Model':<10} {'Accuracy':<10} {'Latency':<10}")

for model, scores in results.items():
    print(f"{model:<10} {scores.get('accuracy', 0):<10.2f} {scores.get('latency', 0):<10}")

print("\n=== Ranking ===")
for i, model in enumerate(ranking, 1):
    print(f"{i}. {model}")
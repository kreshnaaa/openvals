# OpenVals

OpenVals is an the evaluation + trust infrastructure for LLMs, SLMs, local AI, private AI, and public AI designed to help organizations measure, compare, and trust AI models before deployment.

    > Evaluate. Benchmark. Trust. Deploy with Confidence.


![PyPI - Version](https://img.shields.io/pypi/v/openvals)
![Python](https://img.shields.io/pypi/pyversions/openvals)
![License](https://img.shields.io/github/license/vishwanathakuthota/openvals)
![Repo Size](https://img.shields.io/github/repo-size/vishwanathakuthota/openvals)
![Last Commit](https://img.shields.io/github/last-commit/vishwanathakuthota/openvals)

## 🚀 Why OpenVals?

AI models are powerful—but without proper validation, they are unpredictable, insecure, and hard to trust. Most AI evaluation tools stop at metrics.

OpenVals exists to solve that.

It provides a structured way to:

- ✅ Aligns evaluation with business objectives
- ✅ Supports deployment decision-making
- ✅ Quantifies trust, risk, and performance
- ✅ Evaluate model performance  
- ✅ Benchmark multiple models  
- ✅ Normalize and compare results  
- ✅ Introduce trust before deployment  

This is especially critical for:

- ✅ LLMs and generative AI  
- ✅ Enterprise AI systems  
- ✅ Regulated industries  
- ✅ Security-sensitive environments

### Most AI models look great in demos—but fail in production.

OpenVals answers:

* Which model is actually best for your use case?
* How do models compare beyond just “accuracy”?
* Can I trust this model in production?
* Which model is fastest, safest, and most reliable?

---
## Core Capabilities
### 1. Model Evaluation
Evaluate model outputs against structured datasets using:

- Accuracy
- Semantic similarity
- Latency

### 2. Multi-Model Benchmarking
Compare multiple models under the same conditions:

- Side-by-side evaluation
- Normalized scoring
- Model ranking
- Performance insights

### 3. Scoring Engine

Weighted scoring aligned to business priorities:

Trust Score = Σ (wᵢ × mᵢ)

- Customize weights per use case  

- Balance accuracy, cost, and latency 

### 4. Extensible Architecture

- Plug-and-play model adapters
- Custom metrics support
- Scalable evaluation pipelines

### 5. Recommendation Engine
- Suggests best model for your dataset
- Tradeoff-aware ranking (speed vs accuracy vs safety)
- Use-case based model selection (coming next version)

---
## Installation

    pip install openvals 

---
# ⚡ Quick Start

### 1. Run Evaluation
```python
from openvals.core.evaluator import Evaluator
from openvals.datasets.loader import load_dataset
from openvals.models.ollama_model import OllamaModel

dataset = load_dataset("examples/sample_eval.json")

model = OllamaModel("llama3")

evaluator = Evaluator(model, dataset)

result = evaluator.run()

print(result["overall_score"])
```

---
### 2. Run Multi-Model Benchmark
```python
from openvals.benchmarking.runner import BenchmarkRunner
from openvals.models.ollama_model import OllamaModel
from openvals.datasets.loader import load_dataset

dataset = load_dataset("examples/sample_eval.json")

models = {
    "llama2": OllamaModel("llama2"),
    "llama3": OllamaModel("llama3"),
    "mistral": OllamaModel("mistral")
}

runner = BenchmarkRunner(models, dataset)

results = runner.run()

print(results)
```

---
## 📊 Example Output
```code
=== FINAL RANKING ===
1. mistral   (0.91)
2. llama3    (0.87)
3. llama2    (0.84)
```
## Key Features

* ⚡ Multi-model benchmarking (Ollama + APIs)
* 📊 Multi-metric evaluation system
* 🧠 Semantic + accuracy hybrid scoring
* ⏱️ Latency-aware ranking
* 🔐 Reliability + safety scoring
* 📈 Normalized comparison engine
* 🎯 Recommendation engine (next phase)

## Built For

* AI engineers
* ML teams
* SaaS companies using LLMs
* Enterprises validating models
* AI governance & compliance teams

## 🔬 Metrics Explained

### Performance Metrics

This project uses the following key performance indicators to evaluate system output and efficiency.

### Core Metrics

| Metric | Meaning |
| :--- | :--- |
| **Accuracy** | Exact / relaxed match scoring |
| **Semantic** | Meaning similarity |
| **Latency** | Response speed |
| **Reliability** | Stability of output |
| **Safety** | Risk/unsafe content detection |

### Usage
These metrics are applied during the evaluation phase to ensure consistent and high-quality results across all modules.

---
# API Usage

```python
from openvals.core.evaluator import Evaluator
from openvals.models.dummy_model import DummyModel
from openvals.datasets.loader import load_dataset

dataset = load_dataset("examples/sample_eval.json")
model = DummyModel()

evaluator = Evaluator(model, dataset)
result = evaluator.run()

print(result)
```
---


## Multi-Model Benchmarking Example

```python 
from openvals.models.dummy_model import DummyModel
from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.benchmarking.ranking import rank_models

models = {
    "model_a": DummyModel(),
    "model_b": DummyModel()
}

runner = BenchmarkRunner(models, dataset)
results = runner.run()

normalized = normalize_scores(results)

ranking = rank_models(normalized, {
    "accuracy": 0.5,
    "semantic": 0.3,
    "latency": 0.2
})

print(ranking)
```

---
## 🏗️ Project Structure
```tree
openvals/
│
├── core/              # Evaluation engine
├── models/            # Model adapters
├── datasets/          # Dataset loading & schema
├── metrics/           # Evaluation metrics
├── benchmarking/      # Multi-model benchmarking layer
├── scoring/           # Scoring logic
├── safety/            # Risk & safety checks (WIP)
├── reporting/         # Output & reports (WIP)
├── cli.py             # Command-line interface
```

---
## 🚀 Roadmap
### v0.1 (Current)
* Core evaluator
* Benchmarking engine
* Ollama integration

### v0.2
* Advanced normalization
* Dataset expansion tools
* Better semantic scoring

### v0.3
* Recommendation engine
* Explainability layer (WHY model is best)

### v1.0
* SaaS API layer
* Dashboard
* Enterprise model governance

---
## 🧠 Philosophy & Vision
> “If you can’t measure it, you can’t trust it.”

**OpenVals** is building the trust layer for AI systems.

---
## Mission 
Our mission is to build the essential trust layer for AI systems, ensuring they remain transparent, reliable, and safe **for a better future of humanity**.

---
## 🚀 Roadmap
### v0.1 (Current)
* Core evaluator
* Benchmarking engine
* Ollama integration

### v0.2
* Advanced normalization
* Dataset expansion tools
* Better semantic scoring

### v0.3
* Recommendation engine
* Explainability layer (WHY model is best)

### v1.0
* SaaS API layer
* Dashboard
* Enterprise model governance
Use code with caution.
Would you like me to add an Installation section to help users get started with the Core Evaluator?

---
## Contributing
Contributions are welcome.

- Fork the repo
- Create a feature branch
- Submit a pull request

---
## License
MIT License

---
## Backed by
Developed as part of DrPinnacle’s AI Trust & Validation Initiative, focused on building secure, scalable, and trustworthy AI systems.

* [Dr. Pinnacle](https://drpinnacle.com)
* [OpenValidations](https://openvalidations.com)

---
## ⚡ Final Thought
AI models are easy to build.
Trusting them is the hard part.
OpenVals exists to solve that.

# OpenVals

OpenVals is an open evaluation and benchmarking framework for LLMs, SLMs, and AI systems, designed to help organizations measure, compare, and trust AI models before deployment.

    > Evaluate. Benchmark. Trust. Deploy with Confidence.


![PyPI](https://img.shields.io/pypi/v/openvals)
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

---

## Core Capabilities

### 1. Model Evaluation
Evaluate model outputs against structured datasets using:

- Accuracy
- Semantic similarity
- Latency

---

### 2. Multi-Model Benchmarking
Compare multiple models under the same conditions:

- Side-by-side evaluation
- Normalized scoring
- Model ranking
- Performance insights

---

### 3. Scoring Engine

Weighted scoring aligned to business priorities:

Trust Score = Σ (wᵢ × mᵢ)

- Customize weights per use case  

- Balance accuracy, cost, and latency 

---

### 4. Extensible Architecture

- Plug-and-play model adapters
- Custom metrics support
- Scalable evaluation pipelines

---

## Installation

    pip install openvals 

---

## ⚡ Quick Start

### 1. Run Evaluation

    openvals run --dataset examples/sample_eval.json 

---

### 2. Run Multi-Model Benchmark

    openvals benchmark --dataset examples/sample_eval.json 

---

## 🧪 Example Dataset

json [   {     "id": "1",     "input": "hello",     "expected_output": "olleh"   } ] 

---

## API Usage

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

## Roadmap

### v0.3
- [ ] OpenAI / Ollama / HuggingFace adapters
- [ ] Config-driven benchmarking (config.yaml)
- [ ] Parallel execution

### v0.4
- [ ] Safety layer (prompt injection, hallucination)
- [ ] Cost tracking
- [ ] Advanced reporting

### v1.0
- [ ] Trust Score engine
- [ ] Industry-specific benchmarks
- [ ] Certification layer

---

## Vision

OpenVals is evolving into:

    > A Trust Layer for AI Systems

Where organizations can answer:

- Which model should be deployed?
- Is it safe?
- Is it aligned with business goals?
- Can it be trusted in production?

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

openvalidations.com 

---

## ⚡ Final Thought

AI models are easy to build.

Trusting them is the hard part.

OpenVals exists to solve that.

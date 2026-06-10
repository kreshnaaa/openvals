# OpenVals

> AI Trust Intelligence Platform for LLMs, SLMs, Private AI, and Enterprise AI Systems

**Evaluate • Benchmark • Trust Intelligence**

OpenVals is an enterprise-grade AI evaluation and trust platform designed to help organizations measure, compare, validate, and deploy AI systems with confidence.

Unlike traditional AI benchmarks that focus only on accuracy, OpenVals evaluates performance, trustworthiness, factuality, reliability, safety, hallucination risk, governance readiness, and deployment confidence.

---

## Why OpenVals?

Most AI models perform well in demonstrations.

Production environments require something different:

- Can the model be trusted?
- Is the response factually correct?
- How reliable is the model under repeated execution?
- What is the hallucination risk?
- Is the dataset itself trustworthy?
- Is the model ready for enterprise deployment?

OpenVals was built to answer these questions.

---

## Core Platform Capabilities

### AI Evaluation Engine

Evaluate AI systems using multiple dimensions:

- Accuracy
- Semantic Similarity
- Reliability
- Safety
- Consistency
- Variance
- Latency
- Factuality
- Hallucination Risk

---

### Decision Reliability Score (DRS)

OpenVals introduces the Decision Reliability Score (DRS), a deployment-focused trust metric designed to determine whether an AI system is suitable for real-world production environments.

DRS combines:

- Accuracy
- Semantic Intelligence
- Reliability
- Safety
- Consistency
- Variance
- Latency
- Hallucination Risk
- Factuality

Traditional leaderboards answer:

"Which model scored highest?"

DRS answers:

"Which model can be trusted in production?"

---

### Factuality Engine

OpenVals includes a dedicated factuality scoring engine capable of:

- Semantic factual alignment
- Numeric consistency validation
- Contradiction detection
- Factual risk classification

Output:

```text
Factuality Score
Risk Level
Issues Detected
```

---

### Hallucination Probability Index (HPI)

OpenVals introduces HPI (Hallucination Probability Index).

HPI estimates the probability that a model response contains hallucinated or unreliable content.

Risk Levels:

- Low
- Medium
- High
- Critical

---

### Dataset Intelligence

Trust the dataset before trusting the model.

Dataset Validation CLI includes:

- Schema validation
- Quality validation
- Duplicate detection
- Missing field detection
- Dataset Health Score (DHS)

Examples:

```bash
openvals validate-dataset finance
```

```bash
openvals validate-dataset ./customer_dataset.json
```

```bash
openvals validate-dataset ./customer_dataset.csv
```

---

### Multi-Model Benchmarking

Compare multiple models under identical conditions.

Supported:

- Ollama Models
- Local Models
- Private AI
- Enterprise AI
- Future API-based providers

Capabilities:

- Side-by-side comparison
- Normalized ranking
- DRS ranking
- Trust Intelligence reporting

---

### Parallel Execution Engine

OpenVals supports parallel model execution for faster benchmarking.

```bash
openvals benchmark \
  --dataset finance \
  --models mistral,llama3 \
  --parallel \
  --max-workers 2
```

Benefits:

- Reduced benchmark runtime
- Better scalability
- Future SaaS readiness

---

### Executive Reporting

OpenVals generates executive-grade reports:

#### Dashboard Report

```text
report.html
```

Includes:

- Trust Dashboard
- DRS Ranking
- Operational Insights
- Governance Readiness
- Risk Analysis
- Visual Analytics

#### Sample-Level Evaluation Report

```text
sample_report.html
```

Includes:

- Prompt
- Expected Output
- Model Output
- Accuracy
- Semantic
- Factuality
- Hallucination Risk
- Safety
- Latency

---

## Supported Benchmark Domains

Current datasets:

- Finance
- Healthcare
- Cybersecurity

Future:

- Legal
- Insurance
- Manufacturing
- Retail
- Enterprise Operations
- Software Engineering

---

## Installation

```bash
pip install openvals
```

---

## Quick Start

Benchmark multiple models:

```bash
openvals benchmark \
  --dataset finance \
  --models mistral,llama3 \
  --config finance
```

Validate a dataset:

```bash
openvals validate-dataset finance
```

List available datasets:

```bash
openvals datasets
```

Show version:

```bash
openvals version
```

---

## OpenVals Architecture

```text
Dataset
   ↓

Dataset Validation
   ↓

Evaluation Engine
   ↓

Trust Intelligence
   ↓

DRS
   ↓

Recommendation Engine
   ↓

Executive Reporting
```

---

## Roadmap

### v0.4.0

- Parallel Model Execution
- Reporting Refactor
- Sample-Level Drilldown
- Dataset Validation CLI
- Judge Layer Foundation

### v0.5.0

- LLM-as-a-Judge
- Trust Index (TI)
- Governance Analytics
- PDF Reports
- REST APIs
- Evaluation History
- Hugging Face Dataset Integration
- Kaggle Dataset Integration

### Future

- OpenVals Cloud
- Enterprise Governance
- Continuous AI Validation
- Team Workspaces
- Trust Intelligence Dashboard
- AI Certification Framework

---

## Vision

OpenVals is building the Trust Intelligence Layer for AI.

The future of AI is not determined by which model is largest.

The future belongs to AI systems that can be measured, validated, governed, and trusted.

---

## Contributing

Contributions are welcome.

- Fork the repository
- Create a feature branch
- Submit a pull request

---

## License

Dr.Pinnacle Community Edition License (DPCL-CE) v1.0

---

## Developed By

DrPinnacle -- AI Trust, Validation & Governance Initiative

[DrPinnacle](drpinnacle.com)

[OpenVals](openvalidations.com)
---

## Keywords

AI Evaluation Platform, AI Trust Platform, LLM Evaluation, AI Benchmarking, AI Governance, AI Validation, Factuality Scoring, Hallucination Detection, DRS Score, AI Trust Intelligence, Enterprise AI Validation, Private AI Evaluation, Ollama Benchmarking, AI Reliability Testing, OpenVals, Vishwanath Akuthota
# OpenVals Metric Registry

Version: v0.3.0

---

## Purpose

The Metric Registry defines all supported evaluation metrics used throughout OpenVals.

Each metric contains:

* Category
* Direction
* Weightability
* Description

---

# Performance Metrics

## Accuracy

Category:

```text
performance
```

Direction:

```text
higher
```

Description:

Measures exact correctness of output compared with expected response.

---

## Semantic Similarity

Category:

```text
performance
```

Direction:

```text
higher
```

Description:

Measures meaning similarity between model output and expected output.

---

## Latency

Category:

```text
performance
```

Direction:

```text
lower
```

Description:

Measures response time for model generation.

---

# Trust Metrics

## Reliability

Category:

```text
trust
```

Direction:

```text
higher
```

Description:

Measures output stability across multiple executions.

---

## Safety

Category:

```text
trust
```

Direction:

```text
higher
```

Description:

Measures potentially harmful or unsafe behavior.

---

## Consistency

Category:

```text
trust
```

Direction:

```text
higher
```

Description:

Measures repeatability of outputs.

---

## Variance

Category:

```text
trust
```

Direction:

```text
lower
```

Description:

Measures output fluctuation.

---

## Hallucination (HPI)

Category:

```text
trust
```

Direction:

```text
lower
```

Description:

Measures probability of fabricated information.

Components:

* Overconfidence Detection
* Fabrication Signals
* Semantic Risk
* Variance Signals

---

## Factuality

Category:

```text
trust
```

Direction:

```text
higher
```

Description:

Measures factual correctness relative to expected answer.

Signals:

* Semantic Agreement
* Numeric Consistency
* Contradiction Detection

---

# Infrastructure Metrics

## Compute

Category:

```text
infrastructure
```

Direction:

```text
lower
```

Description:

Compute resource consumption.

---

## Energy

Category:

```text
infrastructure
```

Direction:

```text
lower
```

Description:

Energy usage estimation.

---

## Carbon

Category:

```text
infrastructure
```

Direction:

```text
lower
```

Description:

Estimated carbon footprint.

---

# Metric Lifecycle

Metrics move through:

```text
Registry
    ↓
Evaluator
    ↓
Normalization
    ↓
Weighted Score
    ↓
DRS
    ↓
Recommendation Engine
    ↓
Reporting
```

---

# Future Metrics

Planned for v0.4+:

* Judge Score
* RAG Faithfulness
* Context Precision
* Agent Reliability
* Tool Usage Accuracy
* Governance Compliance
* Security Posture

---

# Registry Status

Current Metrics:

```text
11
```

Production Metrics:

```text
8
```

Architecture Version:

```text
1.0
```
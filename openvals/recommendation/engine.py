from openvals.recommendation.profiles import PROFILES


class RecommendationEngine:
    def __init__(self, results):
        self.results = results

    # 🧮 Score model based on use-case weights
    def _score_model(self, metrics, weights):
        score = 0.0

        for k, w in weights.items():
            val = metrics.get(k, 0)

            # ⏱️ Normalize latency (lower is better)
            if k == "latency":
                val = 1 / (1 + val)

            score += w * val

        return score

    # 🧠 Generate explanation (top contributing factors)
    def _generate_reason(self, model_data, weights):
        metrics = model_data["metrics"]

        top_factors = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]

        reasons = []
        for factor, _ in top_factors:
            val = metrics.get(factor, 0)
            reasons.append(f"{factor}={round(val, 2)}")

        return "Strong performance in: " + ", ".join(reasons)

    # ⚖️ Trade-off analysis vs next best model
    def _tradeoffs(self, ranked):
        best = ranked[0]
        second = ranked[1] if len(ranked) > 1 else None

        if not second:
            return "No comparison available"

        tradeoffs = []

        for metric in best["metrics"]:
            b = best["metrics"].get(metric, 0)
            s = second["metrics"].get(metric, 0)

            if metric == "latency":
                if b > s:
                    tradeoffs.append("slightly slower than alternatives")
            else:
                if b < s:
                    tradeoffs.append(f"lower {metric} than some models")

        return ", ".join(tradeoffs) if tradeoffs else "Balanced performance"

    # 🚨 Risk detection
    def _risk_flags(self, model_data):
        m = model_data["metrics"]

        risks = []

        if m.get("reliability", 1) < 0.7:
            risks.append("Low reliability")

        if m.get("consistency", 1) < 0.7:
            risks.append("Inconsistent outputs")

        if m.get("safety", 1) < 0.8:
            risks.append("Potential safety concerns")

        if m.get("latency", 0) > 15000:
            risks.append("High latency")

        return risks if risks else ["No major risks"]

    # 🎯 Confidence score (combined trust)
    def _confidence(self, score, drs):
        return round(score * drs, 3)

    # 🚀 Main recommendation method
    def recommend(self, use_case="default"):

        weights = PROFILES.get(use_case, PROFILES["default"])

        scored = []

        for model_name, data in self.results.items():
            metrics = data.get("metrics", {})
            drs = data.get("drs_score", 0)

            score = self._score_model(metrics, weights)

            scored.append({
                "model": model_name,
                "score": round(score, 3),
                "drs": round(drs, 3),
                "metrics": metrics
            })

        # 🏆 Rank models
        ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

        best = ranked[0]

        return {
            "recommended_model": best["model"],
            "score": best["score"],
            "drs": best["drs"],
            "confidence": self._confidence(best["score"], best["drs"]),
            "reason": self._generate_reason(best, weights),
            "tradeoffs": self._tradeoffs(ranked),
            "risks": self._risk_flags(best),
            "ranking": ranked
        }
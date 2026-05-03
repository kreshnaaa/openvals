from openvals.recommendation.profiles import PROFILES


class RecommendationEngine:

    def __init__(self, results):
        self.results = results

    def _score_model(self, metrics, weights):
        score = 0.0

        for k, w in weights.items():
            val = metrics.get(k, 0)

            # latency inversion (lower is better)
            if k == "latency":
                val = 1 / (1 + val)

            score += w * val

        return score

    def recommend(self, use_case="default"):

        weights = PROFILES.get(use_case, PROFILES["default"])

        scored = []

        for model_name, data in self.results.items():
            metrics = data["metrics"]
            drs = data.get("drs_score", 0)

            score = self._score_model(metrics, weights)

            scored.append({
                "model": model_name,
                "score": round(score, 3),
                "drs": drs,
                "metrics": metrics
            })

        # sort by score
        ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

        best = ranked[0]

        return {
            "recommended_model": best["model"],
            "score": best["score"],
            "drs": best["drs"],
            "reason": self._generate_reason(best, weights),
            "ranking": ranked
        }

    def _generate_reason(self, model_data, weights):

        metrics = model_data["metrics"]

        top_factors = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]

        reasons = []
        for factor, _ in top_factors:
            val = metrics.get(factor, 0)
            reasons.append(f"{factor}={round(val, 2)}")

        return "Strong performance in: " + ", ".join(reasons)
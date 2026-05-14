from openvals.recommendation.profiles import PROFILES

from openvals.explainability.insights import generate_insights
from openvals.explainability.summary import generate_summary
from openvals.intelligence.deployment import deployment_readiness


class RecommendationEngine:

    def __init__(self, results):
        self.results = results

    # =====================================================
    # SCORE MODEL BASED ON USE-CASE WEIGHTS
    # =====================================================

    def _score_model(self, metrics, weights):

        score = 0.0

        for k, w in weights.items():

            val = metrics.get(k, 0)

            # Lower latency is better
            if k == "latency":
                val = 1 / (1 + val)

            score += w * val

        return round(score, 3)

    # =====================================================
    # GENERATE EXPLANATION
    # =====================================================

    def _generate_reason(self, model_data):

        metrics = model_data["metrics"]

        strengths = []

        if metrics.get("accuracy", 0) >= 0.80:
            strengths.append("strong accuracy")

        if metrics.get("semantic", 0) >= 0.80:
            strengths.append("high semantic understanding")

        if metrics.get("reliability", 0) >= 0.80:
            strengths.append("strong reliability")

        if metrics.get("safety", 0) >= 0.85:
            strengths.append("good safety characteristics")

        if metrics.get("consistency", 0) >= 0.80:
            strengths.append("consistent responses")

        if metrics.get("variance", 1) <= 0.20:
            strengths.append("low output variance")

        if metrics.get("latency", 999999) <= 2000:
            strengths.append("fast response time")

        if strengths:
            return (
                f"{model_data['model']} demonstrated "
                + ", ".join(strengths)
                + "."
            )

        return (
            f"{model_data['model']} achieved balanced "
            f"performance across evaluation metrics."
        )

    # =====================================================
    # TRADEOFF ANALYSIS
    # =====================================================

    def _tradeoffs(self, ranked):

        if len(ranked) < 2:
            return "No comparison available"

        best = ranked[0]
        second = ranked[1]

        tradeoffs = []

        for metric in best["metrics"]:

            b = best["metrics"].get(metric, 0)
            s = second["metrics"].get(metric, 0)

            if metric == "latency":

                if b > s:
                    tradeoffs.append(
                        "slightly slower than alternatives"
                    )

            else:

                if b < s:
                    tradeoffs.append(
                        f"lower {metric} than competing models"
                    )

        return (
            ", ".join(tradeoffs)
            if tradeoffs
            else "Balanced performance"
        )

    # =====================================================
    # DETAILED TRADEOFFS
    # =====================================================

    def _tradeoffs_detail(self, metrics):

        details = []

        if metrics.get("latency", 0) > 5000:
            details.append(
                "Higher latency may affect real-time workloads."
            )

        if metrics.get("variance", 0) > 0.30:
            details.append(
                "Elevated variance may impact output predictability."
            )

        if metrics.get("semantic", 0) < 0.70:
            details.append(
                "Semantic alignment weaker on complex tasks."
            )

        if metrics.get("safety", 1) < 0.80:
            details.append(
                "Additional safety validation recommended."
            )

        if not details:
            details.append(
                "Balanced operational tradeoffs observed."
            )

        return details

    # =====================================================
    # RISK DETECTION
    # =====================================================

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

    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    def _detect_anomalies(self, metrics):

        anomalies = []

        if (
            metrics.get("accuracy", 0) > 0.85
            and metrics.get("reliability", 1) < 0.50
        ):
            anomalies.append(
                "High accuracy but unstable reliability detected."
            )

        if (
            metrics.get("semantic", 0) > 0.80
            and metrics.get("variance", 0) > 0.40
        ):
            anomalies.append(
                "Strong semantic capability with unstable outputs."
            )

        if metrics.get("latency", 0) > 10000:
            anomalies.append(
                "Extreme latency detected under evaluation."
            )

        if metrics.get("safety", 1) < 0.60:
            anomalies.append(
                "Unsafe generation patterns detected."
            )

        return (
            anomalies
            if anomalies
            else ["No major anomalies detected"]
        )

    # =====================================================
    # CONFIDENCE SCORE
    # =====================================================

    def _confidence(self, score, drs):

        confidence = score * drs

        return round(confidence, 3)

    # =====================================================
    # MAIN RECOMMENDATION METHOD
    # =====================================================

    def recommend(self, use_case="default"):

        weights = PROFILES.get(
            use_case,
            PROFILES["default"]
        )

        scored = []

        # =================================================
        # SCORE EACH MODEL
        # =================================================

        for model_name, data in self.results.items():

            metrics = data.get("metrics", {})

            drs = data.get("drs_score", 0)

            score = self._score_model(
                metrics,
                weights
            )

            insights = generate_insights(metrics)

            summary = generate_summary(
                model_name,
                metrics,
                drs
            )

            tradeoffs_detail = self._tradeoffs_detail(
                metrics
            )

            anomalies = self._detect_anomalies(
                metrics
            )

            deployment = deployment_readiness(
                metrics
            )

            scored.append({

                "model": model_name,

                "score": round(score, 3),

                "drs": round(drs, 3),

                "metrics": metrics,

                "insights": insights,

                "summary": summary,

                "tradeoffs_detail": tradeoffs_detail,

                "anomalies": anomalies,

                "deployment": deployment

            })

        # =================================================
        # RANK MODELS
        # =================================================

        ranked = sorted(
            scored,
            key=lambda x: x["score"],
            reverse=True
        )

        best = ranked[0]

        # =================================================
        # FINAL RESPONSE
        # =================================================

        return {

            "recommended_model": best["model"],

            "score": best["score"],

            "drs": best["drs"],

            "confidence": self._confidence(
                best["score"],
                best["drs"]
            ),

            "reason": self._generate_reason(
                best
            ),

            "tradeoffs": self._tradeoffs(
                ranked
            ),

            "tradeoffs_detail": best[
                "tradeoffs_detail"
            ],

            "risks": self._risk_flags(
                best
            ),

            "summary": best["summary"],

            "insights": best["insights"],

            "anomalies": best["anomalies"],

            "deployment": best["deployment"],

            "ranking": ranked
        }

def compare(results):
    return {
        model: {
            "score": data["overall_score"],
            "metrics": data["metrics"]
        }
        for model, data in results.items()
    }

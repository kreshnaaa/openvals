
import argparse
from openvals.datasets.loader import load_dataset
from openvals.models.dummy_model import DummyModel
from openvals.core.evaluator import Evaluator
from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.benchmarking.ranking import rank_models

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--dataset", required=True)

    bench_parser = subparsers.add_parser("benchmark")
    bench_parser.add_argument("--dataset", required=True)

    args = parser.parse_args()
    dataset = load_dataset(args.dataset)

    if args.command == "run":
        model = DummyModel()
        evaluator = Evaluator(model, dataset)
        print(evaluator.run())

    elif args.command == "benchmark":
        models = {"m1": DummyModel(), "m2": DummyModel()}
        runner = BenchmarkRunner(models, dataset)
        results = runner.run()
        normalized = normalize_scores(results)
        ranking = rank_models(normalized, {"accuracy": 0.5, "semantic": 0.3, "latency": 0.2})
        print({"results": results, "ranking": ranking})

if __name__ == "__main__":
    main()

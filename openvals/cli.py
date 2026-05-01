
import argparse
import yaml
import os
from openvals.datasets.loader import load_dataset
from openvals.models.dummy_model import DummyModel
from openvals.models.ollama_model import OllamaModel
from openvals.models.openai_model import OpenAIModel
from openvals.core.evaluator import Evaluator
from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.benchmarking.ranking import rank_models


def load_config(config_path: str) -> dict:
    """Load benchmark configuration from a YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def build_models_from_config(config: dict) -> dict:
    """Build model instances based on config file definitions."""
    models = {}
    for model_cfg in config.get("models", []):
        name = model_cfg["name"]
        model_type = model_cfg["type"]

        if model_type == "ollama":
            if "model_name" not in model_cfg or "base_url" not in model_cfg:
                raise ValueError(f"Missing 'model_name' or 'base_url' for Ollama model '{name}' in config.")
            models[name] = OllamaModel(
                model_name=model_cfg["model_name"],
                base_url=model_cfg["base_url"]
            )
        elif model_type == "openai":
            if "api_key" not in model_cfg or "model_name" not in model_cfg:
                raise ValueError(f"Missing 'api_key' or 'model_name' for OpenAI model '{name}' in config.")
            # Use optional base_url from config if present, otherwise default is used in model
            base_url = model_cfg.get("base_url", "https://api.openai.com/v1")
            models[name] = OpenAIModel(
                api_key=model_cfg["api_key"],
                model_name=model_cfg["model_name"],
                base_url=base_url
            )
        else:
            raise ValueError(f"Unknown model type: '{model_type}'.")

    return models


def parse_model_string(model_str: str) -> tuple:
    """
    Parse a model string in the format 'type:model_name@extra'.
    - For ollama: 'ollama:name@url'
    - For openai: 'openai:name@api_key'
    """
    try:
        m_type, rest = model_str.split(":", 1)
        if "@" not in rest:
            raise ValueError(f"Missing extra info (URL or API Key) in '{model_str}'. Use 'type:name@extra'.")
        
        name, extra = rest.split("@", 1)

        if m_type == "ollama":
            return OllamaModel(model_name=name, base_url=extra), f"ollama_{name}"
        elif m_type == "openai":
            # Support both 'name@api_key' (default URL) and 'name@api_key@url'
            if "@" in extra:
                api_key, url = extra.split("@", 1)
            else:
                api_key, url = extra, "https://api.openai.com/v1"
            return OpenAIModel(api_key=api_key, model_name=name, base_url=url), f"openai_{name}"
        else:
            raise ValueError(f"Unknown model type: {m_type}")
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid model format. Use 'type:name@extra'. Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="OpenVals — AI Model Evaluation & Benchmarking")
    subparsers = parser.add_subparsers(dest="command")

    # run command
    run_parser = subparsers.add_parser("run", help="Evaluate a single model")
    run_parser.add_argument("--dataset", required=True, help="Path to dataset JSON file")
    run_parser.add_argument("--model", required=True, help="Model in format 'type:name@extra' (e.g. ollama:llama3.1@http://localhost:11434)")

    # benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Benchmark multiple models")
    bench_parser.add_argument("--dataset", required=True, help="Path to dataset JSON file")
    bench_parser.add_argument("--config",  help="Path to benchmark config YAML file")
    bench_parser.add_argument("--model",   action="append", help="Add model (format 'type:name@extra')")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    dataset = load_dataset(args.dataset)

    if args.command == "run":
        model, _ = parse_model_string(args.model)
        evaluator = Evaluator(model, dataset)
        print(evaluator.run())

    elif args.command == "benchmark":
        models = {}
        # Previous method: Default weights
        default_weights = {"accuracy": 0.5, "semantic": 0.3, "latency": 0.2}
        weights = default_weights

        if args.config:
            config  = load_config(args.config)
            weights = config.get("weights", default_weights)
            models  = build_models_from_config(config)
        
        if args.model:
            for m_str in args.model:
                m_inst, m_name = parse_model_string(m_str)
                models[m_name] = m_inst

        if not models:
            print("Error: No models provided. Use --model or --config.")
            return

        print(f"Starting benchmark for {len(models)} models: {list(models.keys())}")

        # Run benchmark with parallel execution enabled
        runner     = BenchmarkRunner(models, dataset, weights=weights, parallel=True)
        results    = runner.run()
        normalized = normalize_scores(results)
        ranking    = rank_models(normalized, weights)

        print({"results": results, "ranking": ranking})


if __name__ == "__main__":
    main()

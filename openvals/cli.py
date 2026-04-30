
import argparse
from openvals.datasets.loader import load_dataset
from openvals.models.dummy_model import DummyModel
from openvals.core.evaluator import Evaluator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    dataset = load_dataset(args.dataset)
    model = DummyModel()
    evaluator = Evaluator(model, dataset)

    result = evaluator.run()
    print(result)

if __name__ == "__main__":
    main()

from setuptools import setup, find_packages

setup(
    name="openvals",
    version="0.3.100",
    author="Vishwanath Akuthota",
    description=(

        "Enterprise AI Evaluation & Trust Framework "

        "for benchmarking, validating, and trusting LLMs"

    ),
    url="https://github.com/vishwanathakuthota/openvals",
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "typer",
        "rich",
        "matplotlib",
        "seaborn",
        "jupyterlab",
        "notebook",
        "plotly",
        "sentence-transformers"

    ],

    entry_points={
        "console_scripts": [
            "openvals=openvals.cli.app:main"
        ]
    }
)

from setuptools import setup, find_packages

setup(
    name="openvals",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy", "pandas", "scikit-learn"],
    entry_points={
        "console_scripts": [
            "openvals=openvals.cli:main"
        ]
    }
)

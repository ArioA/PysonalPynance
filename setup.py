from setuptools import setup, find_packages

setup(
    name="pynance",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={},
)


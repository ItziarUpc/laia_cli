from setuptools import setup, find_packages

setup(
    name="laia",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "laia=laia.cli:main",
        ]
    },
)
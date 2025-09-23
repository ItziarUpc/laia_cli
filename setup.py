from setuptools import setup, find_packages

setup(
    name="laia-cli",
    version="0.1.4",
    description="CLI de la librería de LAIA",
    author="Itziar",
    author_email="itziar.mensa08@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pydantic>=2.0",
        "fastapi>=0.100.0",
        "pymongo>=4.0",
        "bcrypt>=4.0",
        "nest_asyncio>=1.5",
        "python-dotenv>=1.0",
        "uvicorn>=0.22",
        "rdflib>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "laia=laia_cli.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
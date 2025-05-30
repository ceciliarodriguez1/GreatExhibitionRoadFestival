from setuptools import setup, find_packages

setup(
    name="movesense-data-collector",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "bleak",
        "pandas",
        "numpy",
        "asyncio",
    ],
)
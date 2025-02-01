from setuptools import setup, find_packages
import os

# Read the README file safely
def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()

setup(
    name="keywords_finder",
    version="0.1",
    author="Lucy Maber",
    author_email="your_email@example.com",
    description="A Python package for efficient keyword searching using Aho-Corasick.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/LucyMaber/KeywordsFinder",
    packages=find_packages(include=["keywords_finder", "keywords_finder.*"]),
    install_requires=[
        "pyahocorasick"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

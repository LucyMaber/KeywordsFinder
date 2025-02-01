from setuptools import setup, find_packages

setup(
    name="keywords_finder",
    version="0.1",
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LucyMaber/KeywordsFinder",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

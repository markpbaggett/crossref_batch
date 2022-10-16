from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()


setup(
    name="UTK Crossref Batch Procedures",
    description="Documentation generation for describing batch procedures in Crossref",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="Mark Baggett",
    author_email="mbagget1@utk.edu",
    maintainer_email="mbagget1@utk.edu",
    url="https://github.com/markpbaggett/crossref_batch_",
    packages=find_packages(),
    extras_require={
        "docs": [
            "sphinx >= 5.0.2",
            "sphinx-rtd-theme >= 1.0.0",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    keywords=["libraries", "documentation", "crossref", "dois"],
)

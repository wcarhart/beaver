import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="beaver",
    version="1.0.0",
    description="An animal that eats logs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wcarhart/beaver",
    author="Will Carhart",
    author_email="wcarhart@sandiego.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["beaver"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "beaver=beaver.__main__:main",
        ]
    },
)
from setuptools import setup, find_packages

setup(
    name="blincus-test",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    author="Quixines",
    author_email="nathan@quixines.com",
    description="A Blincus payment processing package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nathan2002-hash/test-blincus-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyshopify",
    version="0.9.4",
    author="Joseph Trabulsy",
    author_email="webdjoe@gmail.com",
    description="Shopify Order API library with containeriezed MS SQL database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyshopify",
    project_urls={
        "Bug Tracker": "https://github.com/pyshopify/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click>=8.0.1',
        'numpy>=1.20.3',
        'pandas>=1.2.4',
        'python-dateutil',
        'requests>=2.20',
        'six'
    ],
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=["test"]),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'shopify_cli = pyshopify.cli:cli_runner',
        ],
    }
)

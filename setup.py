#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="psi-runtime-sdk",
    version="0.1.0",
    packages=find_packages(include=["psi_runtime_sdk", "psi_runtime_sdk.*"]),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "pyyaml>=6.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "api": ["fastapi>=0.68.0", "uvicorn>=0.15.0"],
        "cli": ["click>=8.0.0"],
        "dev": ["pytest>=6.0.0", "black>=21.5b2", "isort>=5.9.1"],
        "test": ["pytest>=6.0.0", "pytest-cov>=2.12.0"],
    },
    python_requires=">=3.8",
    author="AI開發團隊",
    author_email="info@example.com",
    description="量子啟發式推理與語義場分析SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/psi-runtime-sdk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

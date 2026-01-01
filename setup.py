"""
Setup script for Chatterbox TTS
This allows the package to be installed in development mode
"""
from setuptools import setup, find_packages

setup(
    name="chatterbox-tts",
    version="1.0.0",
    description="Chatterbox TTS - Text-to-Speech with Voice Cloning",
    author="ResembleAI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0,<1.26.0",
        "librosa==0.11.0",
        "s3tokenizer",
        "torch==2.7.1",
        "torchaudio==2.7.1",
        "transformers==4.46.3",
        "diffusers==0.29.0",
        "resemble-perth==1.0.1",
        "conformer==0.3.2",
        "safetensors==0.5.3",
        "pykakasi==2.3.0",
        "gradio==5.44.1",
    ],
)

"""
Setup file for Python Image Generator
"""
from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="python-imagegen",
    version="1.0.0",
    description="API để tạo ảnh từ HTML với background từ Pexels",
    author="MMOMarketplace",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.11",
)


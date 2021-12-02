#-*-coding:utf-8-*-
from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as f:
    desc = f.read()


setup(
    name="gvcode",
    version="0.0.5",
    description="A useful verification code generation tool.",
    long_description=desc,
    long_description_content_type="text/markdown",
    license="GNU",
    author="Msky",
    author_email="690126048@qq.com",
    url="https://github.com/miloira/gvcode",
    packages=find_packages(),
    install_requires=["pillow"]
)
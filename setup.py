#-*-coding:utf-8-*-
from setuptools import setup, find_packages
import os
import shutil
import platform

with open("README.md","r",encoding="utf-8") as f:
    desc = f.read()

system = platform.system()
if system == 'Linux':
    path = '/usr/share/fonts/'
    if not os.path.exists(path):
        os.mkdir(path)
    shutil.copy('gvcode/fonts/arial.ttf', path + 'arial.ttf')

setup(
    name="gvcode",
    version="0.0.3",
    description="A useful verification code generation tool.",
    long_description=desc,
    long_description_content_type="text/markdown",
    license="GNU",
    author="Msky",
    author_email="690126048@qq.com",
    url="https://github.com/zhangmingming-chb/verificationcode",
    packages=find_packages(),
    install_requires=["pillow"]
)
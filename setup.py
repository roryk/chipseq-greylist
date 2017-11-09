#!/usr/bin/env python
from setuptools import setup
version = "1.0.1"

install_requires = ["pandas", "numpy", "scipy", "statsmodels"] 

scripts = ['scripts/chipseq-greylist']

setup(name="chipseq-greylist",
      version=version,
      author="Rory Kirchner",
      author_email="roryk@alum.mit.edu",
      description="python implementation of GreyListChIP",
      license="MIT",
      url="https://github.com/roryk/chipesq-greylist",
      scripts=scripts,
      install_requires=install_requires)

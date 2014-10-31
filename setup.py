#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

setup(
    name='coursera-downloader',
    version='0.1',
    packages=find_packages(),
    scripts=[
        'coursera-dl.py',
    ])

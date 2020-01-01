from os.path import join, dirname, realpath
from setuptools import setup
import sys

setup(
    name="simple_games",
    py_modules=["src"],
    version='0.1',
    install_requires=["numpy", "gym"],
    description="A suite of extremely simple (kinderleicht) games",
    author="Rive Sunder",
)

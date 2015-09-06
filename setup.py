import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "peacock",
    version = "0.0.7",
    author = "Travis Hoppe",
    author_email = "travis.hoppe+peacock@gmail.com",
    description = ("An implementation of the Swagger 2.0 spec in python."),
    license = "MIT",
    keywords = "swagger traits",
    packages=['peacock'], #, 'tests'],
    long_description=read('README.md'),
    install_requires=['traits'],
)

from setuptools import setup
from setuptools import find_packages

from flask_blog import __version__ as version

# version = pkg_resources.require("MyProject")[0].version


def readme():
    with open("README.md") as f:
        return f.read()


def required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="flask-blog",
    version=version,
    description="flask blog.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="flask blog",
    author="André P. Santos",
    author_email="andreztz@gmail.com",
    url="https://github.com/andreztz/flask-blog",
    license="MIT",
    packages=find_packages(),
    install_requires=required(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

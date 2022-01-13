import os
import sys
import setuptools

sys.path[0:0] = ['jtex']
from version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jtex",
    description="Jinja-style templating for LaTeX documents by Curvenote",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    entry_points='''
        [console_scripts]
        jtex=jtex.__main__:main
    ''',
    url="http://curvenote.com",
    version=__version__,
    author="iooxa inc.",
    author_email="hi@curvenote.com",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "typer",
        "jinja2",
        "pykwalify",
        "pyyaml",
        "requests",
        "mergedeep"
    ],
    python_requires=">=3.7",
)

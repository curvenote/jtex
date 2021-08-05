import sys
import setuptools

sys.path[0:0] = ['curvenote_template']
from version import __version__

def readme():
    with open("README.rst") as file:
        return file.read()


setuptools.setup(
    name="curvenote_template",
    description="Jinja-style templating for LaTeX documents by Curvenote",
    long_description=readme(),
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
        curvenote_template=curvenote_template.__main__:main
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
        "pyyaml"
    ],
    python_requires=">=3.7",
)

from setuptools import setup, find_packages
from pyplagiarism.version import __version__

def readme():
    with open('README.rst') as f:
        return f.read()


__name__ = "pyplagiarism"
__author__ = "Julian Blank"
__url__ = "https://github.com/julesy89/pyplagiarism"

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email="blankjul@egr.msu.edu",
    description="Plagiarism Tool for Source Code",
    long_description=readme(),
    url=__url__,
    license='Apache License 2.0',
    keywords="optimization",
    install_requires=["numpy", "pycode_similar", "plotly", "mistune", "pygments", "diff-match-patch"],
    packages=find_packages(exclude=['tests', 'doc']),
    include_package_data=True,
    platforms='any',
)

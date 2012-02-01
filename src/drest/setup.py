
from setuptools import setup, find_packages
import sys, os

VERSION = '0.9.2'

setup(name='drest',
    version=VERSION,
    description="dREST API Client Library",
    long_description="dREST API Client Library",
    classifiers=[], 
    keywords='rest api',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/drest/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'httplib2',
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        ],
    )

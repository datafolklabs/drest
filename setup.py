
from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.1'

setup(name='drest',
    version=VERSION,
    description="dREST API Client Framework",
    long_description="dREST API Client Framework",
    classifiers=[], 
    keywords='rest api framework',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/drest',
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

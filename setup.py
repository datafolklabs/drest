
from setuptools import setup, find_packages
import sys, os

VERSION = '0.9.13'

setup(name='drest',
    version=VERSION,
    description="dRest API Client Library for Python",
    long_description="dRest API Client Library for Python",
    classifiers=[],
    keywords='rest api',
    author='BJ Dierkes',
    author_email='derks@datafolklabs.com',
    url='http://github.com/datafolklabs/drest/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >=1.0",
        #
        ### Required for testing
        # "nose",
        # "coverage",
        #
        ### Required to function
        'httplib2',
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        ],
    )

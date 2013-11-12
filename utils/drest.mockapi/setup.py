
from setuptools import setup, find_packages
import sys, os

VERSION = '0.9.13'

setup(name='drest.mockapi',
    version=VERSION,
    description="dRest Mock API for Testing",
    long_description="dRest Mock API for Testing",
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/drest',
    license='None',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        "django",
        "django-tastypie",
        "python-digest",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[],
    )

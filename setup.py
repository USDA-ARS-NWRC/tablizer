#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

# requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Mark Robertson",
    author_email='mark.robertson@usda.gov',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Summarizes DataFrames and 2D arrays to database or csv.",
    install_requires=required,
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tablizer',
    name='tablizer',
    packages=find_packages(include=['tablizer']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/robertson-mark/tablizer',
    version='0.2.2',
    zip_safe=False,
)

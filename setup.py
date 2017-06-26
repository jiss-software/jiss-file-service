#!/usr/bin/env python

from setuptools import setup

setup(
    name='FileService',
    description='File upload/distribution component.',
    version='1.0',
    author='Anton Iskov',
    author_email='aiskov@jiss-software.com',
    url='http://www.jiss-software.com',
    packages=[
        'handler'
    ],
    install_requires=[
        'tornado==4.2.1',
        'motor==1.1'
    ]
)

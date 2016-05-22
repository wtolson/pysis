#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='pysis',
    version='0.6.0',
    description='Toolkit for using USGS Isis in Python.',
    long_description=readme + '\n\n' + history,
    author='Trevor Olson',
    author_email='trevor@heytrevor.com',
    url='https://github.com/wtolson/pysis',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pvl',
        'six',
    ],
    license='BSD',
    zip_safe=False,
    keywords='pysis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'alpha_vantage_downloader',
    version = '0.0.5',
    url = 'https://github.com/fricative/alpha_vantage_downloader',
    author = 'fricative',
    author_email = 'keye906@yahoo.com',
    description = 'A simple wrapper around alpha vantage api',
    packages = find_packages(),
    install_requires = ['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
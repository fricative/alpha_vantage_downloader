# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'alpha_vantage_downloader',
    version = '0.0.1',
    url = 'https://github.com/fricative/alpha_vantage_downloader.git',
    author = 'fricative',
    author_email = 'keye906@yahoo.com',
    description = 'A simple wrapper around alpha vantage api',
    packages = ['alpha_vantage_downloader'],
    install_requires = ['pandas'],
)
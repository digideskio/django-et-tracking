#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django_et_tracking',
    version='0.0.5',
    description='Exact Target reporting',
    author='JBA',
    author_email='lex@jbadigital.com',
    url='https://github.com/jbadigital/django-et-tracking',
    packages=find_packages(exclude=['tests']),
    install_requires=['django']
)

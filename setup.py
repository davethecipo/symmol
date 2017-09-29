#!/usr/bin/env python

from setuptools import setup

setup(name='symmol',
      version='0.1',
      description='Build symmetric molecules',
      author='Davide Olianas',
      author_email='admin@davideolianas.com',
      url='',
      modules=['symmol'],
      install_requires=['numpy'],
      extras_require={
          'dev': [ 'Sphinx' ]
      }
     )
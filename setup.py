#!/usr/bin/env python
from setuptools import setup

setup(
	name='hisp',
	version='1.0.0a',
	install_requires=['ply==3.3'],
    description='HTML generator. Lisp syntax. Django integration.',
	author='Nate Soares',
	author_email='nate@natesoares.com',
    license='MIT',
	# url='http://hisp.natesoares.com',
	packages=[
        'hisp', 'hisp.libraries', 'hisp.tables',
        'hisp.loaders', 'hisp.management', 'hisp.management.commands',
    ],
)

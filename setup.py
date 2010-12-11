#!/usr/bin/env python
from distutils.core import setup

setup(
	name='hisp',
	version='0.1a',
	requires=['ply'],
    description='HISP: Html-Lisp language',
	author='Nate Soares',
	author_email='nate@natesoares.com',
	# url='http://hisp.natesoares.com',
	packages=[
        'hisp', 'hisp.tables', 'hisp.libraries',
        'hisp.loaders', 'hisp.management', 'hisp.management.commands',
    ],
)

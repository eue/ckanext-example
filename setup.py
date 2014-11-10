from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-example',
	version=version,
	description="Example harvester plugin for CKAN",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Fraunhofer FOKUS',
	author_email='ogdd-harvesting@fokus.fraunhofer.de',
	url='https://github.com/fraunhoferfokus/ckanext-govdatade',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.example'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]	
	rostock_test_harvester=ckanext.example.harvester:RostockTestHarvester
	""",
)

from setuptools import setup
from setuptools import find_packages
import sys
import os

version = '0.1'
requires = ['transaction']

setup(name='ZMQTxn',
      version=version,
      description="A transaction datamanager for use with ZeroMQ",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ZeroMQ JSON',
      author='Whit "whitmo" Morris',
      author_email='whit at surveymonkey.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

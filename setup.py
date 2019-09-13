"""Setup script for Podswamp

See:
https://github.com/FatConan/podswamp
"""

# To use a consistent encoding
# pylint: disable=redefined-builtin
from codecs import open
from os import path

# Apparently you should always prefer setuptools over distutils
from setuptools import setup, find_packages

# pylint: disable=invalid-name
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='podswamp',
      version='2018.1.3.1.1a0',
      description='Generates a simple listing site from a provided libsyn rss feed and configuration',
      long_description=long_description,

      # The project's main homepage
      url='https://github.com/FatConan/podswamp',

      # Author's details
      author='FatConan',
      author_email='ian@headwillcollapse.net',
      include_package_data=True,
      license='MIT',

      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          ],

      # What does this project relate to?
      keywords='web html rss podcasts static content',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),

      # List run-time dependencies here.
      # https://packaging.python.org/en/latest/requirements.html
      install_requires=['jinja2', 'nltk'],
      extras_require={
          'dev': ['check-manifest'],
          'test': ['coverage'],
      },
      entry_points={
          'console_scripts': ['podswamp=podswamp.__main__:main']
      }
 )

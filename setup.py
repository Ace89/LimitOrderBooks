#  create a setup_file
#  https://python-packaging.readthedocs.io/en/latest/minimal.html

from setuptools import setup

setup(
    name='LimitOrderBooks',
    version='0.1',
    description='Library designed to analyse limit order book data',
    url='Github',
    author='Awais Talib',
    author_email='Awais.Talib@kellogg.ox.ac.uk',
    license='None Required',
    packages=['numpy, pandas'],
    zip_safe=False
)

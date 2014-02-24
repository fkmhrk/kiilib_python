from setuptools import setup

setup(
    name='kiilib',
    version='0.1dev',
    packages=['kiilib','kiilib/demo'],
    license='Apache 2.0',
    long_description=open('README.rst').read(),
    setup_requires=['nose>=1.0'],
)

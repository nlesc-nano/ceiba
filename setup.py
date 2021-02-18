#!/usr/bin/env python
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(HERE, 'ceiba', '__version__.py')) as f:
    exec(f.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='ceiba',
    version=version['__version__'],
    description="Server to handle the molecular properties",
    long_description=readme + '\n\n',
    author="Felipe Zapata",
    author_email='f.zapata@esciencecenter.nl',
    url='https://github.com/nlesc-nano/ceiba',
    packages=[
        'ceiba',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='ceiba',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': ['ceiba=ceiba.app:run']},
    data_files=[('citation/ceiba', ['CITATION.cff'])],
    install_requires=[
        'aiohttp==3.7.3', 'more-itertools', 'tartiflette', 'tartiflette-aiohttp',
        'pandas', 'pymongo', 'requests'],
    extras_require={
        'test': ['coverage', 'mypy', 'pycodestyle', 'pytest>=3.9',
                 'pytest-asyncio', 'pytest-cov', 'pytest-mock'],
        'docs': ['sphinx', 'sphinx_rtd_theme']
    }
)

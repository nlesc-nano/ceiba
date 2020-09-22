#!/usr/bin/env python
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(HERE, 'properties_database', '__version__.py')) as f:
    exec(f.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='properties_server',
    version=version,
    description="Server to handle the molecular properties",
    long_description=readme + '\n\n',
    author="Felipe Zapata",
    author_email='f.zapata@esciencecenter.nl',
    url='https://github.com/nlesc-nano/properties_server',
    packages=[
        'properties_server',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='properties_server',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    data_files=[('citation/properties_server', ['CITATION.cff'])]
    install_requires=[],
    extras_require={
        'test': ['coverage', 'mypy', 'pycodestyle', 'pytest>=3.9', 'pytest-cov'
                 ],
        'doc': ['sphinx', 'sphinx-autodoc-typehints', 'sphinx_rtd_theme',
                'nbsphinx']
    }
)

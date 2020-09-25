#!/usr/bin/env python
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(HERE, 'insilico-server', '__version__.py')) as f:
    exec(f.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='insilico-server',
    version=version,
    description="Server to handle the molecular properties",
    long_description=readme + '\n\n',
    author="Felipe Zapata",
    author_email='f.zapata@esciencecenter.nl',
    url='https://github.com/nlesc-nano/insilico-server',
    packages=[
        'insilico-server',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='insilico-server',
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
        'console_scripts': ['insilico-server=insilico-server.app:run']},
    data_files=[('citation/insilico-server', ['CITATION.cff'])],
    install_requires=['tartiflette', 'tartiflette-aiohttp',
                      'properties_database@git+https://github.com/nlesc-nano/insilico-server@master#egg=properties_database'
                      ],
    extras_require={
        'test': ['coverage', 'mypy', 'pycodestyle', 'pytest>=3.9', 'pytest-cov'
                 ],
        'doc': ['sphinx', 'sphinx-autodoc-typehints', 'sphinx_rtd_theme',
                'nbsphinx']
    }
)

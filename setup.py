#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='cloudflareapi',
    version='0.1',
    author='Cristian Steib',
    author_email='cristiansteib@gmail.com',
    url='https://github.com/cristiansteib/cloudflareapi',
    install_requires=open('requirements.txt').read().splitlines(),
    description='Cloudflare api',
    package_data={'resources': ['*', '**/*', '**/**/*']},
    license='Propietary',
    packages=find_packages()
)
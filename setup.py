# coding=UTF-8
import os
import io

from glob import glob
from setuptools import setup, find_packages
from os.path import splitext, basename

version = open('.VERSION').read()

requirements_file = [line.strip()
                     for line in open('requirements.txt').readlines()
                     if line.strip() and not line.startswith('#')]
requirements = requirements_file


def get_readme(filename="README.md"):
    this = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(this, filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name='certbot-dns-gransy',
    version=version,
    description='Gransy DNS Authenticator plugin for Certbot',
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author='Lukáš Vasek',
    url='https://github.com/bilak/certbot-dns-gransy',
    license='Apache license 2.0',
    keywords='certbot dns gransy dns-01 authenticator api',

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,

    entry_points={
        'certbot.plugins': [
            'dns-gransy = certbot_dns_gransy.dns_gransy:Authenticator',
        ],
    },

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: Apache 2.0",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],

    data_files=[
        ('', [
            '.VERSION',
            'LICENSE.txt',
            'README.md',
        ]),
    ]
)

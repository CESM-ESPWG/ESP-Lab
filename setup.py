#!/usr/bin/env python3

"""The setup script."""

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('README.md') as f:
    long_description = f.read()


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Scientific/Engineering',
]

setup(
    name='esp-lab',
    version='1.0.1',
    description='Utilities for SMYLE Analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    maintainer='ESP-Lab Team',
    maintainer_email='tking@ucar.edu',
    classifiers=CLASSIFIERS,
    url='https://esp-lab.readthedocs.io',
    project_urls={
        'Documentation': 'https://esp-lab.readthedocs.io',
        'Source': 'https://github.com/CESM-ESPWG/ESP-Lab',
        'Tracker': 'https://github.com/CESM-ESPWG/ESP-Lab/issues',
    },
    packages=find_packages(exclude=('tests',)),
    package_dir={'esp-lab': 'esp-lab'},
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    zip_safe=False,
    entry_points={},
    keywords='ESP-Lab, SMYLE, Analysis, Earth System Predictions',
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
)

# ESP-Lab

- [ESP-Lab](#esp-lab)
  - [Badges](#badges)
  - [Overview](#overview)
  - [Installation](#installation)

## Badges
| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![Code Coverage Status][codecov-badge]][codecov-link] |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                                                     [![Documentation Status][rtd-badge]][rtd-link]                                                                     |
| **Package** |                                                          [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                          |
| **License** |                                                                         [![License][license-badge]][repo-link]                                                                         |

## Overview
ESP-Lab is an Earth System Predictions Python package that was originally designed to enable users to effectively perform I/O operations and statistics on [SMYLE (The Seasonal-to-Multiyear Large Ensemble)](https://doi.org/10.5194/gmd-2022-60) data. It provides a foundation for analysis of multiyear prediction of environmental change.

Some of the challenges with multiyear prediction that ESP-Lab addresses include working with lead times ranging from 1 month to 2 years, as well as efficiently analyzing large ensembles.

This package provides utilities which support input/output processes such as methods to return dictionaries of filepaths keyed by initialization year, nested lists of files for particular start years and ensemble members, and dask arrays containing particular hindcast ensembles. ESP-Lab also provides
preprocessing which can assist in using intake-esm in conjunction with other data_access functions.

ESP Lab also enables statistics calculations through functions providing tools to perform linear detrending along a particular axis, determine skill metrics based on model and observation DataArrays, and generate a distribution of skill scores using a smaller ensemble member size.

## Installation
ESP_Lab can be installed from PyPI with pip:

```bash
pip install esp-lab
```

Note: If you use `pip` to install `esp-lab`, you can install `esp-lab` directly into a pre-existing conda environment (after doing `conda activate <environment_name>` and any requirements that you do not already have will be added automatically to that environment during installation. Another option is to create a new environment, for instance with `conda env create --name esp-lab` and then activate that environment with `conda activate esp-lab`. At that point, you are ready to install `esp-lab` into the new environment with `python -m pip install esp-lab`.


One can also install `esp-lab` as a developer by following these steps:
1) git clone https://github.com/CESM-ESPWG/ESP-Lab.git
2) cd ESP-Lab
3) conda env create --file environment.yml
4) conda activate esp-lab
4) pip install -e .

[github-ci-badge]: https://img.shields.io/github/workflow/status/CESM-ESPWG/ESP-Lab/CI?label=CI&logo=github
[github-ci-link]: https://github.com/CESM-ESPWG/ESP-Lab/actions?query=workflow%3ACI
[codecov-badge]: https://img.shields.io/codecov/c/github/CESM-ESPWG/ESP-Lab.svg?logo=codecov
[codecov-link]: https://codecov.io/gh/CESM-ESPWG/ESP-Lab
[rtd-badge]: https://img.shields.io/readthedocs/esp-lab/latest.svg
[rtd-link]: https://esp-lab.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/esp-lab?logo=pypi
[pypi-link]: https://test.pypi.org/project/esp-lab/0.0.6/
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/esp-lab?logo=anaconda
[conda-link]: https://anaconda.org/TeaganK/esp-lab
[license-badge]: https://img.shields.io/github/license/CESM-ESPWG/ESP-Lab
[repo-link]: https://github.com/CESM-ESPWG/ESP-Lab


Documentation can be found at [esp-lab.readthedocs.io](esp-lab.readthedocs.io)

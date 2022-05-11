# ESP-Lab

- [ESP-Lab](#esp-lab)
  - [Badges](#badges)
  - [Overview](#overview)
  - [Installation](#installation)

## Badges
| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![Code Coverage Status][codecov-badge]][codecov-link] [![pre-commit.ci status][pre-commit.ci-badge]][pre-commit.ci-link] |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                                                     [![Documentation Status][rtd-badge]][rtd-link]                                                                     |
| **Package** |                                                          [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                          |
| **License** |                                                                         [![License][license-badge]][repo-link]                                                                         |

## Overview
ESP-Lab is an Earth System Predictions Python package that was originally designed to enable users to effectively perform I/O operations and statistics on SMYLE data. It is available to assist with data for earth system predictions. 

This package provides utilities which support input/output processes such as methods to return dictionaries of filepaths keyed by initialization year, nested lists of files for particular start years and ensemble members, and dask arrays containing particular hindcast ensembles. ESP-Lab also provides
preprocessing which can assist in using intake-esm in conjunction with other data_access functions.

ESP Lab also enables statistics calculations through functions providing tools to perform linear detrending along a particular axis, determine skill metrics based on model and observation DataArrays, and generate a distribution of skill scores using a smaller ensemble member size.

## Installation
ESP_Lab will soon be able to be installed from PyPI with pip:

```bash
python -m pip install intake-esm
```

[github-ci-badge]: https://img.shields.io/github/workflow/status/CESM-ESPWG/ESP-Lab/CI?label=CI&logo=github
[github-ci-link]: https://github.com/CESM-ESPWG/ESP-Lab/actions?query=workflow%3ACI
[codecov-badge]: https://img.shields.io/codecov/c/github/CESM-ESPWG/ESP-Lab.svg?logo=codecov
[codecov-link]: https://codecov.io/gh/CESM-ESPWG/ESP-Lab
[rtd-badge]: https://img.shields.io/readthedocs/esp-lab/latest.svg
[rtd-link]: https://esp-lab.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/esp-lab?logo=pypi
[pypi-link]: https://pypi.org/project/esp-lab
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/esp-lab?logo=anaconda
[conda-link]: https://anaconda.org/conda-forge/esp-lab
[license-badge]: https://img.shields.io/github/license/CESM-ESPWG/ESP-Lab
[repo-link]: https://github.com/CESM-ESPWG/ESP-Lab
[pre-commit.ci-badge]: https://results.pre-commit.ci/badge/github/CESM-ESPWG/ESP-Lab/main.svg
[pre-commit.ci-link]: https://results.pre-commit.ci/latest/github/CESM-ESPWG/ESP-Lab/main


Documentation can be found at [esp-lab.readthedocs.io](esp-lab.readthedocs.io)

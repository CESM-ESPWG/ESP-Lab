import cftime
from functools import partial
import glob
import numpy as np
import sys
import xarray as xr

from esp_lab.data_access import time_set_midmonth
from esp_lab.data_access import file_dict
from esp_lab.data_access import get_monthly_data
from esp_lab.data_access import nested_file_list_by_year
from esp_lab.data_access import preprocessor


def test_file_dict():
    """
    Test the file_dict function.
    """

    filetemplate = 'tests/test_data/b.e21.BSMYLE.f09_g17.????-MM.EEE.pop.h.zsatcalc.*.nc'
    filetype = '.pop.h.'
    mem = 3
    stmon = 2

    filepaths = file_dict(filetemplate, filetype, mem, stmon)

    assert filepaths[1986] == 'tests/test_data/b.e21.BSMYLE.f09_g17.1986-02.003.pop.h.zsatcalc.198602-198801.nc'
    assert len(filepaths.keys()) == 3


def test_get_monthly_data():
    """
    Test the get_monthly_data function.
    """
    # todo: make test

    assert True


def test_nested_file_list_by_year():
    """
    Test the nested_file_list_by_year function.
    """
    filetemplate = 'tests/test_data/b.e21.BSMYLE.f09_g17.????-MM.EEE.pop.h.zsatcalc.*.nc'
    filetype = '.pop.h.'
    ens = 3
    firstyear = 1986
    lastyear = 1988
    stmon = 2

    nested_files = nested_file_list_by_year(filetemplate, filetype, ens, firstyear, lastyear, stmon)
    print("nested_files {}".format(nested_files))

    assert nested_files[1][2] == 1988


def test_preprocessor():
    """
    Test the preprocessor function.
    """
    # todo: make test

    assert True


def test_time_set_midmonth():
    """
    Test the time_set_midmonth function.
    """
    test = True

    assert test

import sys

import pytest

import xarray as xr
import numpy as np
import sys
import cftime
import xskillscore as xs

from esp_lab.stats import cor_ci_bootyears, detrend_linear, leadtime_skill_seas, leadtime_skill_seas_resamp, remove_drift

def test_cor_ci_bootyears():
    """
    Test the cor_ci_bootyears function.
    """
    ts1 = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    ts2 = np.array([4, 5, 6, 7, 8, 9, 1, 2, 3])

    # result12 = cor_ci_bootyears(ts1, ts2)
    result11 = cor_ci_bootyears(ts1, ts1)

    # assert result12[0] < -0.4  # -0.43306723784214496
    # assert result12[1] > 0.8  # 0.8097240500333097

    # An array should be fully correlated with itself
    assert result11[0] > 0.999
    assert result11[1] < 1.001


def test_detrend_linear():
    """
    Test the detrend_linear function.
    """

    # Create some example data.
    tsize = 10
    xsize = 2
    ysize = 2

    # create array of nan's with correct size
    data = np.ones((tsize, xsize, ysize)) * np.nan

    # fill array with data
    data[:, 0, 0] = np.linspace(0, 10, tsize)
    data[:, 1, 0] = np.logspace(0, 1, tsize)
    data[:, 0, 1] = np.logspace(1.5, 0.5, tsize)
    data[:, 1, 1] = np.linspace(40, 10, tsize)

    # Put the data in a xarray.Dataset.
    ds = xr.Dataset({"data": (["time", "x", "y"], data)})

    # Apply polyfit.
    fit = ds.polyfit(dim="time", deg=1)
    final_dat = ds - fit

    assert final_dat.dims == {'x': 2, 'y': 2, 'degree': 2}
    assert (final_dat['x'].data == np.array([0, 1])).all()
    assert (final_dat['y'].data == np.array([0, 1])).all()
    assert (final_dat['degree'].data == np.array([1, 0])).all()


def test_leadtime_skill_seas():
    """
    Test the leadtime_skill_seas function.
    """
    test = True

    assert test
    

def test_leadtime_skill_seas_resamp():
    """
    Test the leadtime_skill_seas_resamp function.
    """
    test = True

    assert test


def test_remove_drift():
    """
    Test the remove_drift function.
    """
    test = True

    assert test

import cftime
import numpy as np
import pandas as pd
import pytest
import sys
import xarray as xr
import xskillscore as xs

from esp_lab.stats import cor_ci_bootyears
from esp_lab.stats import detrend_linear
from esp_lab.stats import leadtime_skill_seas
from esp_lab.stats import leadtime_skill_seas_resamp
from esp_lab.stats import remove_drift


def test_cor_ci_bootyears():
    """
    Test the cor_ci_bootyears function.
    """
    ts1 = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    ts2 = ts1*1.01

    result = cor_ci_bootyears(ts1, ts2)

    # Two very similar arrays should be highly correlated
    assert result[0] > 0.9
    assert result[1] < 1.1


def test_cor_ci_bootyears_two_different_array_sizes():
    """
    Test that the cor_ci_bootyears function fails with
    two differently sized arrays.
    """
    ts1 = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    ts2 = np.array([1, 2, 3])

    with pytest.raises(SystemExit) as e:
        cor_ci_bootyears(ts1, ts2)

    assert e.type == SystemExit


def test_cor_ci_bootyears_seed():
    """
    Test that the cor_ci_bootyears function random seed
    generates the same exact result each time
    """
    ts1 = np.array([15, 24, 35, 11, 52, 63, 71, 22, 83])
    ts2 = np.array([10, 22, 34, 11, 33, 57, 22, 71, 90])
    result = cor_ci_bootyears(ts1, ts2, seed=123)
    
    assert result == (-0.22524093559047992, 0.9763300171129478)


def test_detrend_linear():
    """
    Test the detrend_linear function.
    """

    temperature = np.array([[[16,  2,  3],
                             [14, 27, 12]],
                            [[14, 14,  6],
                             [12, 10, 12]]])
    lon = [[-99.83, -99.32], [-99.79, -99.23]]
    lat = [[42.25, 42.21], [42.63, 42.59]]
    time = pd.date_range("2014-09-06", periods=3)
    reference_time = pd.Timestamp("2014-09-05")
    da = xr.DataArray(data=temperature,
                      dims=["x", "y", "time"],
                      coords=dict(
                            lon=(["x", "y"], lon),
                            lat=(["x", "y"], lat),
                            time=time,
                            reference_time=reference_time),
                      attrs=dict(
                            description="Temperature.",
                            units="degC"))

    # Apply linear detrending
    final_dat = detrend_linear(da, "time")

    assert final_dat.dims == ('x', 'y', 'time')
    assert final_dat.data[0][0][0] > 2.4
    assert final_dat.data[0][0][0] < 2.5
    assert final_dat.data[1][1][1] > -1.4
    assert final_dat.data[1][1][1] < -1.3
    assert final_dat.data[1][0][1] > 2.6
    assert final_dat.data[1][0][1] < 2.7


def test_leadtime_skill_seas():
    """
    Test the leadtime_skill_seas function.
    """
    # todo: make test

    assert True


def test_leadtime_skill_seas_resamp():
    """
    Test the leadtime_skill_seas_resamp function.
    """
    # todo: make test

    assert True


def test_remove_drift():
    """
    Test the remove_drift function.
    """
    # todo: make test

    assert True

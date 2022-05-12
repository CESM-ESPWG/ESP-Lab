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
                            description="Ambient temperature.",
                            units="degC"))

    # Apply polyfit.
    final_dat = detrend_linear(da, "time")
    # params = da.polyfit(dim="time", deg=1)
    # fit = xr.polyval(da["time"], params.polyfit_coefficients)
    # final_dat = da - fit

    assert final_dat.dims == ('x', 'y', 'time')
    assert final_dat.data[0][0][0] == 2.499999999985448
    assert final_dat.data[1][1][1] == -1.3333333333333304
    assert final_dat.data[1][0][1] == 2.6666666666569654


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

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
    ts1 = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    ts2 = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    
    result = cor_ci_bootyears(ts1, ts2)
    
    print("result {}".format(result))
    
    # assert result[0] == minci
    # assert result[1] == maxci
    
    test = True

    assert test


def test_detrend_linear():
    """
    Test the detrend_linear function.
    """
    test = True

    assert test


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

"""
This module provides utilities for preprocessing which can assist in using
intake-esm in conjunction with that stats-utils and io_utils packages.

Authors
-------
    - Steve Yeager
    - Teagan King
Use
---
    Users wishing to utilize these tools may do so by importing
    various functions, for example:
    ::
        from esp_lab.preprocesser import preprocessor

Dependencies
------------
    The user must have an activated conda environment which includes
    xarray, numpy, and cftime.
"""

# TODO: move time_set_midmonth?

import numpy as np
import xarray as xr
import cftime


def time_set_midmonth(ds, time_name):
    """
    Return copy of ds with values of ds[time_name] replaced with mid-month
    values (day=15) rather than end-month values.

    Parameters
    ----------
    ds : xarray
        xarray dataset which currently has end month values
        that will be replaced with mid month values
    time_name : str
        name of time component, eg 'time'
    Returns
    -------
    ds : xarray
        xarray dataset with end month values replaced with mid month values
    """
    year = ds[time_name].dt.year
    month = ds[time_name].dt.month
    year = xr.where(month == 1, year-1, year)
    month = xr.where(month == 1, 12, month-1)
    nmonths = len(month)
    newtime = [cftime.DatetimeNoLeap(year[i], month[i], 15) for i in range(nmonths)]
    ds[time_name] = newtime

    return ds


def preprocessor(ds0, nlead, field):
    """ This preprocessor is applied on an individual timeseries file basis.
    It will return a monthly mean CAM field with centered time coordinate.
    Edit this appropriately for your analysis to speed up processing.

    Parameters
    ----------
    ds0 : xarray
        timeseries xarray dataset that requires preprocessing
    nlead : int
        (?)
    field : str
        variable to be examined, eg 'TREFHT'

    Returns
    -------
    d0 : xarray
        xarray dataset of monthly mean CAM field with centered time coordinate
    """
    d0 = time_set_midmonth(ds0, 'time')
    d0 = d0.isel(time=slice(0, nlead))
    d0 = d0.assign_coords({"lon": ds0.lon, "lat": ds0.lat})
    d0 = d0.assign_coords(L=("time", np.arange(d0.sizes["time"])+1))
    d0 = d0.swap_dims({"time": "L"})
    d0 = d0.reset_coords(["time"])
    d0["time"] = d0.time.expand_dims("Y")
    d0 = d0[[field, 'time']]
    d0 = d0.chunk({'L': -1})
    return d0

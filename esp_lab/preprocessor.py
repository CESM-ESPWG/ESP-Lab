# TODO: Add docstring here, add parameters/returns, move time_set_midmonth?

import numpy as np
import xarray as xr
import cftime


def time_set_midmonth(ds, time_name):
    """
    Return copy of ds with values of ds[time_name] replaced with mid-month
    values (day=15) rather than end-month values.

    Author: S. Yeager
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

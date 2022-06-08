"""
This module provides utilities which support input/output processes.
Functions in this module can provide methods to return dictionaries
of filepaths keyed by initialization year, nested lists of files
for particular start years and ensemble members, and dask arrays
containing particular hindcast ensembles. This module also provides
preprocessing which can assist in using intake-esm in conjunction
with other data_access functions.

Authors
-------
    - Steve Yeager
Use
---
    Users wishing to utilize these tools may do so by importing
    various functions, for example:
    ::
        from esp-tools.utils.io_utils import file_dict

Dependencies
------------
    The user must have an activated conda environment which includes
    xarray, numpy, glob, and functools.
"""

import cftime
import glob
import numpy as np
import xarray as xr
from functools import partial


def file_dict(filetempl, filetype, mem, stmon):
    """
    Returns a dictionary of filepaths keyed by initialization year,
    for a given experiment, field, ensemble member, and initialization month

    Parameters
    ----------
    filetempl : str
        file template
    filetype : str
        file ending
    mem : int
        ensemble member
    stmon : int
        month

    Returns
    -------
    filepaths : dict
        dictionary containing filepaths keyed by initialization year
    """

    memstr = '{0:03d}'.format(mem)
    monstr = '{0:02d}'.format(stmon)
    filepaths = {}

    filetemp = filetempl.replace('MM', monstr).replace('EEE', memstr)

    # find all the relevant files
    files = sorted(glob.glob(filetemp))

    for file in files:
        # isolate initialization year from the file name
        ystr = file.split(filetype)[0]
        y0 = int(ystr[-11:-7])
        filepaths[y0] = file

    return filepaths


def get_monthly_data(filetemplate, filetype, ens, nlead, field,
                     start_years, stmon, preproc, chunks={}):
    """
    Returns a dask array containing the requested hindcast ensemble.

    Parameters
    ----------
    nfiletemplate : str
        file template
    filetype : str
        file ending
    ens : int
        ensemble member
    nlead : int
        number of months over which data is read; allows for a partial read
        of the data and controls the time dimension of returned dask array
    field : str
        variable to be examined, eg 'TREFHT'
    startyears : list
        list of start years which are integers
    stmon : str
        month
    preproc : func
        preprocessing function
    chunks : dict
        chunks for dask array, defaults to {}

    Returns
    -------
    ds0 : dask array
        dask array containing requested hindcast ensemble
    """

    # Retrieve nested list of files
    file_list, yrs = nested_file_list_by_year(filetemplate, filetype, ens,
                                              start_years, stmon)

    # open xarray dataset, passing in parameters including preprocessing fxn
    ds0 = xr.open_mfdataset(file_list,
                            combine="nested",
                            # concat_dim depends on how file_list is ordered;
                            # inner most list of datasets is combined along "M"
                            # then the outer list is combined along "Y"
                            concat_dim=["Y", "M"],
                            parallel=True,
                            data_vars=[field],
                            coords="minimal",
                            compat="override",
                            preprocess=partial(preproc,
                                               nlead=nlead,
                                               field=field),
                            chunks=chunks)

    # assign final attributes
    ds0["Y"] = start_years
    ds0["M"] = np.arange(ds0.sizes["M"]) + 1

    # reorder into desired format (Y,L,M,...)
    ds0 = ds0.transpose("Y", "L", "M", ...)

    return ds0


def nested_file_list_by_year(filetemplate, filetype, ens, start_years, stmon):
    """
    Retrieves a nested list of files for these start years and ensemble members

    Parameters
    ----------
    filetemplate : str
        file template
    filetype : str
        file ending
    ens : int
        ensemble member
    start_years : list
        list of start years which are integers
    stmon : str
        month

    Returns
    -------
    nested_files: list
        nested list of files
    """

    ens = np.array(range(ens)) + 1
    yrs = start_years
    files = []    # a list of lists, dim0=start_year, dim1=ens
    ix = np.zeros(yrs.shape) + 1

    # loop through all years and ensemble members to retrieve filepaths
    for yy, i in zip(yrs, range(len(yrs))):
        ffs = []  # a list of files for this yy
        file0 = ''
        for ee in ens:
            filepaths = file_dict(filetemplate, filetype, ee, stmon)
            # append file if it is new
            if yy in filepaths.keys():
                file = filepaths[yy]
                if file != file0:
                    ffs.append(file)
                    file0 = file

        # append this ensemble member to files
        if ffs:  # only append if you found files
            files.append(ffs)
        else:
            ix[i] = 0

    nested_files = files, yrs[ix == 1]

    return nested_files


def preprocessor(ds0, nlead, field):
    """
    This preprocessor is applied on an individual timeseries file basis.
    It will return a monthly mean CAM field with centered time coordinate.
    Edit this appropriately for your analysis to speed up processing.

    Parameters
    ----------
    ds0 : xarray
        timeseries xarray dataset that requires preprocessing
    nlead : int
        number of months over which data is read; allows for a partial read
        of the data and controls the time dimension of returned dask array
    field : str
        variable to be examined, eg 'TREFHT'

    Returns
    -------
    d0 : xarray
        xarray dataset of monthly mean CAM field with centered time coordinate
    """

    # set the time to the 15th of the month instead of end of month
    d0 = time_set_midmonth(ds0, 'time')
    # select time slice
    d0 = d0.isel(time=slice(0, nlead))
    # assign longitude, latitude, and time coordinates
    d0 = d0.assign_coords({"lon": ds0.lon, "lat": ds0.lat})
    d0 = d0.assign_coords(L=("time", np.arange(d0.sizes["time"])+1))
    # swap time and L 'temporary' dimensions
    d0 = d0.swap_dims({"time": "L"})
    d0 = d0.reset_coords(["time"])
    d0["time"] = d0.time.expand_dims("Y")
    d0 = d0[[field, 'time']]
    # break xarray into chunks
    d0 = d0.chunk({'L': -1})
    return d0


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

    # retrieve current time
    year = ds[time_name].dt.year
    month = ds[time_name].dt.month
    year = xr.where(month == 1, year-1, year)
    month = xr.where(month == 1, 12, month-1)
    nmonths = len(month)
    # set time to 15th day of month
    newtime = [cftime.DatetimeNoLeap(year[i], month[i], 15) for i in range(nmonths)]
    ds[time_name] = newtime

    return ds

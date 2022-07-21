"""
This module provides utilities to assist in statistics calculations related
to SMYLE analysis. Functions provide tools to perform linear detrending along
a particular axis, determine skill metrics based on model and observation
DataArrays, and generate a distribution of skill scores using a smaller
ensemble member size.

Authors
-------
    - Steve Yeager
    - E. Maroon

Use
---
    Users wishing to utilize these tools may do so by importing
    various functions, for example:
    ::
        from esp-tools.utils.stat_utils import cor_ci_bootyears

Dependencies
------------
    The user must have an activated conda environment which includes
    xarray, numpy, sys, cftime, and xskillscore.
"""

import xarray as xr
import numpy as np
import sys
import cftime
import xskillscore as xs


def cor_ci_bootyears(ts1, ts2, seed=None, nboots=1000, conf=95):
    """
    Determine confidence intervals for correlation scores.

    Parameters
    ----------
    ts1 : array
    ts2 : array
    seed : int (optional)
        seed for random number generation, default None
    nboots : int
        number boots (optional, default 1000)
    conf : float (optional)
        confidence value; defaults to 95

    Returns
    -------
    minci : float
        minimum confidence interval
    maxci : float
        maximum confidence interval
    """

    # calculate min and max percentile
    ptilemin = (100. - conf) / 2.
    ptilemax = conf + (100 - conf) / 2.

    # ensure that the arrays have the same size
    if (ts1.size != ts2.size):
        print("The two arrays must have the same size")
        sys.exit()

    # if provided, use a particular seed for random number generation
    if (seed):
        np.random.seed(seed)

    # retreive uniform random number using sample size
    samplesize = ts1.size
    ranu = np.random.uniform(0, samplesize, nboots * samplesize)
    ranu = np.floor(ranu).astype(int)

    bootdat1 = np.array(ts1[ranu])
    bootdat2 = np.array(ts2[ranu])
    bootdat1 = bootdat1.reshape([samplesize, nboots])
    bootdat2 = bootdat2.reshape([samplesize, nboots])

    # compute the Pearson correlation coefficient between datasets
    bootcor = xr.corr(xr.DataArray(bootdat1),
                      xr.DataArray(bootdat2),
                      dim='dim_0')
    # determine minimum and maximum confidence intervals
    minci = np.percentile(bootcor, ptilemin)
    maxci = np.percentile(bootcor, ptilemax)

    return minci, maxci


def detrend_linear(dat, dim):
    """
    Linear detrend dat along the axis dim.

    Parameters
    ----------
    dat : array
        data which is to be detrended
    dim : str
        dimension along which linear detrending is performed

    Returns
    -------
    dat : array
        detrended array
    """

    # determine parameters
    params = dat.polyfit(dim=dim, deg=1)
    # determine fit
    fit = xr.polyval(dat[dim], params.polyfit_coefficients)
    # linearly detrend data
    dat = dat - fit

    return dat


def leadtime_skill_seas(mod_da, mod_time, obs_da, detrend=False):
    """
    Computes a suite of deterministic skill metrics given two DataArrays
    corresponding to model and observations, which must share the same
    lat/lon coordinates (if any). Assumes time coordinates are compatible
    (can be aligned). Both DataArrays should represent 3-month seasonal
    averages (DJF, MAM, JJA, SON).

    Parameters
    ----------
    mod_da: DataArray
        a seasonally-averaged hindcast DataArray dimensioned (Y,L,M,...)
    mod_time: DataArray
        a hindcast time DataArray dimensioned (Y,L).
        note: assumes mod_time.dt.month
    obs_da: DataArray
        an OBS DataArray dimensioned (season,year,...)
    detrend (optional): bool
        defaults to False; if True, skill scores computed after detrending

    Returns
    -------
    xr_dataset : DataArray
        the mid-month of a 3-month seasonal average (e.g., mon=1 ==> "DJF").
    """

    # default seasons
    seasons = {1: 'DJF', 4: 'MAM', 7: 'JJA', 10: 'SON'}
    corr_list = []
    pval_list = []
    rmse_list = []
    msss_list = []
    rpc_list = []
    # convert L to leadtime values:
    leadtime = mod_da.L - 2

    for i in mod_da.L.values:
        # adjust ensemble time to correct format
        ens_ts = mod_da.sel(L=i).rename({'Y': 'time'})
        ens_time_year = mod_time.sel(L=i).dt.year.data
        ens_time_month = mod_time.sel(L=i).dt.month.data[0]
        obs_ts = obs_da.sel(season=seasons[ens_time_month]).rename({'year': 'time'})
        ens_ts = ens_ts.assign_coords(time=("time", ens_time_year))
        a, b = xr.align(ens_ts, obs_ts)
        # perform linear detrending if detrend is set to True
        if detrend:
            a = detrend_linear(a, 'time')
            b = detrend_linear(b, 'time')
        # calculate statistics
        amean = a.mean('M')
        sigobs = b.std('time')
        sigsig = amean.std('time')
        sigtot = a.std('time').mean('M')
        # compute Pearson's correlation coefficient
        r = xs.pearson_r(amean, b, dim='time')
        rpc = r / (sigsig / sigtot)
        # append skill metrics to relevant lists
        corr_list.append(r)
        rpc_list.append(rpc.where(r > 0))
        rmse_list.append(xs.rmse(amean, b, dim='time') / sigobs)
        msss_list.append(1 - (xs.mse(amean, b, dim='time') / b.var('time')))
        pval_list.append(xs.pearson_r_eff_p_value(amean, b, dim='time'))

    # concatenate various lists along leadtime dimension
    corr = xr.concat(corr_list, leadtime)
    pval = xr.concat(pval_list, leadtime)
    rmse = xr.concat(rmse_list, leadtime)
    msss = xr.concat(msss_list, leadtime)
    rpc = xr.concat(rpc_list, leadtime)

    # create xarray dataset from lists
    xr_dataset = xr.Dataset({'corr': corr, 'pval': pval, 'nrmse': rmse,
                             'msss': msss, 'rpc': rpc})

    return xr_dataset


def leadtime_skill_seas_resamp(mod_da, mod_time, obs_da, sampsize, N, detrend=False):
    """
    Computes a suite of deterministic skill metrics given two DataArrays
    corresponding to model and observations, which must share the same
    lat/lon coordinates (if any). Assumes time coordinates are compatible
    (can be aligned). Both DataArrays should represent 3-month seasonal
    averages (DJF, MAM, JJA, SON).

    Unlike leadtime_skill_seas(), this version resamples the
    mod_da member dimension (M) to generate a distribution of skill scores
    using a smaller ensemble size (N, where N<M). Returns the mean of the
    resampled skill score distribution.

    Parameters
    ----------
    mod_da: DataArray
        a seasonally-averaged hindcast DataArray dimensioned (Y,L,M,...)
    mod_time: DataArray
        a hindcast time DataArray dimensioned (Y,L). Assumes mod_time.dt.month
    obs_da: DataArray
        an OBS DataArray dimensioned (season,year,...)
    sampsize : int
        sample size
    N : int
        maximum dimension for resampling
    detrend : bool (optional)
        defaults to False; if set to True, skill scores will be computed after detrending

    Returns
    -------
    dsout : xarray
        mean of resampled skill score distribution
    """

    dslist = []
    # default seasons
    seasons = {1: 'DJF', 4: 'MAM', 7: 'JJA', 10: 'SON'}
    # convert L to leadtime values:
    leadtime = mod_da.L - 2
    # Perform resampling
    if (not N < mod_da.M.size):
        raise ValueError('ERROR: expecting resampled ensemble size to be less than original')
    mod_da_r = xs.resample_iterations(mod_da.chunk(), sampsize, 'M', dim_max=N)
    for l in mod_da_r.iteration.values:
        # create lists for skill metrics
        corr_list = []
        pval_list = []
        rmse_list = []
        msss_list = []
        rpc_list = []
        # loop through leadtime values
        for i in mod_da.L.values:
            # adjust ensemble time to correct format
            ens_ts = mod_da_r.sel(iteration=l).sel(L=i).rename({'Y': 'time'})
            ens_time_year = mod_time.sel(L=i).dt.year.data
            ens_time_month = mod_time.sel(L=i).dt.month.data[0]
            obs_ts = obs_da.sel(season=seasons[ens_time_month]).rename({'year': 'time'})
            ens_ts = ens_ts.assign_coords(time=("time", ens_time_year))
            a, b = xr.align(ens_ts, obs_ts)
            # perform linear detrending if detrend is set to True
            if detrend:
                a = detrend_linear(a, 'time')
                b = detrend_linear(b, 'time')
            # calculate statistics
            amean = a.mean('M')
            sigobs = b.std('time')
            sigsig = amean.std('time')
            sigtot = a.std('time').mean('M')
            # compute Pearson's correlation coefficient
            r = xs.pearson_r(amean, b, dim='time')
            rpc = r / (sigsig / sigtot)
            # append skill metrics to relevant lists
            corr_list.append(r)
            rpc_list.append(rpc.where(r > 0))
            rmse_list.append(xs.rmse(amean, b, dim='time') / sigobs)
            msss_list.append(1 - (xs.mse(amean, b, dim='time') / b.var('time')))
            pval_list.append(xs.pearson_r_eff_p_value(amean, b, dim='time'))

        # concatenate various lists along leadtime dimension
        corr = xr.concat(corr_list, leadtime)
        pval = xr.concat(pval_list, leadtime)
        rmse = xr.concat(rmse_list, leadtime)
        msss = xr.concat(msss_list, leadtime)
        rpc = xr.concat(rpc_list, leadtime)

        # create xarray dataset from lists and append to dslist
        dslist.append(xr.Dataset({'corr': corr, 'pval': pval, 'rmse': rmse,
                                  'msss': msss, 'rpc': rpc}))

    # concatenate dslist along iteration dimension
    dsout = xr.concat(dslist, dim='iteration').mean('iteration').compute()

    return dsout


def remove_drift(da, da_time, y1, y2):
    """
    Function to convert raw DP DataArray into anomaly DP DataArray
    with leadtime-dependent climatology removed.

    Parameters
    ----------
    da : DP DataArray
        Raw DP DataArray with dimensions (Y,L,M,...)
    da_time : DP DataArray
        Verification time of DP DataArray (Y,L)
    y1 : int
        Start year of climatology
    y2 : int
        End year of climatology

    Returns
    -------
    da_anom : DP DataArray
        De-drifted DP DataArray
    da_climo : DP DataArray
        Leadtime-dependent climatology
    """

    # gather first and last second of first and last year, respectively
    d1 = cftime.DatetimeNoLeap(y1, 1, 1, 0, 0, 0)
    d2 = cftime.DatetimeNoLeap(y2, 12, 31, 23, 59, 59)

    # mask data array outside of selected time
    masked_period = da.where((da_time > d1) & (da_time < d2))
    
    # compute lead-time dependent climatology
    if ('M' in masked_period.dims):
        da_climo = masked_period.mean('M').mean('Y')
    else:
        da_climo = masked_period.mean('Y')

    # De-drifted DP data array is data array with
    # leadtime-dependent climotology subtracted
    da_anom = da - da_climo

    return da_anom, da_climo

def compute_skill_annual(mod_da,mod_time,obs_da,nleadavg=1,nleads=1,resamp=0,detrend=False):
    """
    Computes a suite of skill scores for annual data. Option to use xskillscore resampling to
    compute the mean variance of individual member time series ("sigma_total").
    Assumes mod_time and obs_da.time both contain integer year values.
    """
    corr_list = []; pval_list = []; rmse_list = []; msss_list = []; rpc_list = []
    sigobs_list = []; sigsig_list = []; sigtot_list = []; s2t_list = []
    
    lvals = np.arange(nleadavg)
    lvalsda = xr.DataArray(np.arange(nleads)+1,dims="L",name="L")
    for i in range(nleads):
        leadisel = lvals + i 
        ens_ts = mod_da.isel(L=leadisel).mean('L').rename({'Y':'time'})
        ens_time_year = mod_time.isel(L=leadisel).mean('L')
        ens_ts = ens_ts.assign_coords(time=("time",ens_time_year.data))
        a,b = xr.align(ens_ts,obs_ts)
        b = b - b.mean('time')
        if detrend:
                a = detrend_linear(a,'time')
                b = detrend_linear(b,'time')
        amean = a.mean('M')
        sigobs = b.std('time')
        sigsig = amean.std('time')
        if (resamp>0):
            iterations = resamp
            ens_size = 1
            a_resamp = xs.resample_iterations_idx(a, iterations, 'M', dim_max=ens_size).squeeze()
            sigtot = a_resamp.std('time').mean('iteration')
        else:
            sigtot = a.std('time').mean('M')
        r = xs.pearson_r(amean,b,dim='time')
        rpc = r/(sigsig/sigtot)
        corr_list.append(r)
        rpc_list.append(rpc.where(r>0))
        rmse_list.append(xs.rmse(amean,b,dim='time')/sigobs)
        msss_list.append(1-(xs.mse(amean,b,dim='time')/b.var('time')))
        pval_list.append(xs.pearson_r_eff_p_value(amean,b,dim='time'))
        sigobs_list.append(sigobs)
        sigsig_list.append(sigsig)
        sigtot_list.append(sigtot)
        s2t_list.append(sigsig/sigtot)
    corr = xr.concat(corr_list,lvalsda)
    pval = xr.concat(pval_list,lvalsda)
    rmse = xr.concat(rmse_list,lvalsda)
    msss = xr.concat(msss_list,lvalsda)
    rpc = xr.concat(rpc_list,lvalsda)
    sigo = xr.concat(sigobs_list,lvalsda)
    sigs = xr.concat(sigsig_list,lvalsda)
    sigt = xr.concat(sigtot_list,lvalsda)
    s2t  = xr.concat(s2t_list,lvalsda)
    return xr.Dataset({'corr':corr,'pval':pval,'rmse':rmse,'msss':msss,'rpc':rpc,'sig_obs':sigo,'sig_sig':sigs,'sig_tot':sigt,'s2t':s2t})

def compute_skill_seasonal(mod_da,mod_time,obs_da,climy0,climy1,nleadavg=1,nleads=1,resamp=0,detrend=False,monthly=False):
    """
    Computes a suite of skill scores for annual data. Includes option to use xskillscore resampling to
    compute the mean variance of individual member time series ("sigma_total").
    Assumes mod_time and obs_da.time are cftime arrays with year/month values.
    """
    corr_list = []; pval_list = []; rmse_list = []; msss_list = []; rpc_list = []
    sigobs_list = []; sigsig_list = []; sigtot_list = []; s2t_list = []
    
    # convert L to leadtime values:
    if (monthly):
        lvals = np.arange(nleadavg)*12
    else:
        lvals = np.arange(nleadavg)*4
    lvalsda = xr.DataArray(mod_da.isel(L=slice(0,nleads)).L,dims="L",name="L")
    for i in range(nleads):
        leadisel = lvals + i 
        ens_ts = mod_da.isel(L=leadisel).mean('L').rename({'Y':'time'})
        ens_time_year = mod_time.isel(L=leadisel).mean('L').dt.year
        ens_time_month = mod_time.isel(L=leadisel).mean('L').dt.month.data[0]
        ens_ts = ens_ts.assign_coords(time=("time",ens_time_year.data))
        obsisel = obs_da.time.dt.month==ens_time_month
        obs_seas = obs_da.isel(time=obsisel)
        obs_seas = obs_seas - obs_seas.sel(time=slice(climy0,climy1)).mean('time')
        obs_seas = obs_seas.assign_coords(time=("time",obs_seas.time.dt.year.data))
        if (nleadavg>1):
            obs_seas = obs_seas.rolling(time=nleadavg,min_periods=nleadavg, center=True).mean().dropna('time',how='all')
        a,b = xr.align(ens_ts,obs_seas)
        if detrend:
                a = detrend_linear(a,'time')
                b = detrend_linear(b,'time')
        amean = a.mean('M')
        sigobs = b.std('time')
        sigsig = amean.std('time')
        if (resamp>0):
            iterations = resamp
            ens_size = 1
            a_resamp = xs.resample_iterations_idx(a, iterations, 'M', dim_max=ens_size).squeeze()
            sigtot = a_resamp.std('time').mean('iteration')
        else:
            sigtot = a.std('time').mean('M')
        r = xs.pearson_r(amean,b,dim='time')
        rpc = r/(sigsig/sigtot)
        corr_list.append(r)
        rpc_list.append(rpc.where(r>0))
        rmse_list.append(xs.rmse(amean,b,dim='time')/sigobs)
        msss_list.append(1-(xs.mse(amean,b,dim='time')/b.var('time')))
        pval_list.append(xs.pearson_r_eff_p_value(amean,b,dim='time'))
        sigobs_list.append(sigobs)
        sigsig_list.append(sigsig)
        sigtot_list.append(sigtot)
        s2t_list.append(sigsig/sigtot)
    corr = xr.concat(corr_list,lvalsda)
    pval = xr.concat(pval_list,lvalsda)
    rmse = xr.concat(rmse_list,lvalsda)
    msss = xr.concat(msss_list,lvalsda)
    rpc = xr.concat(rpc_list,lvalsda)
    sigo = xr.concat(sigobs_list,lvalsda)
    sigs = xr.concat(sigsig_list,lvalsda)
    sigt = xr.concat(sigtot_list,lvalsda)
    s2t  = xr.concat(s2t_list,lvalsda)
    return xr.Dataset({'corr':corr,'pval':pval,'rmse':rmse,'msss':msss,'rpc':rpc,'sig_obs':sigo,'sig_sig':sigs,'sig_tot':sigt,'s2t':s2t})


def compute_resampskill_annual(mod_da,mod_time,obs_da,nyear=1,nleads=1,detrend=False,resamp=0,mean=True):
    """
    Computes a suite of skill scores for annual data.
    Assumes mod_time and obs_da.time both contain year values.
    """
    dslist = []
    if (nyear>1):
        obs_ts = obs_da.rolling(time=nyear,min_periods=nyear, center=True).mean().dropna('time')
    lvals = np.arange(nyear)
    lvalsda = xr.DataArray(np.arange(nleads),dims="L",name="L")
    for l in mod_da.iteration.values:
        corr_list = []; pval_list = []; rmse_list = []; msss_list = []; rpc_list = []
        sigobs_list = []; sigsig_list = []; sigtot_list = []; s2t_list = []
        for i in range(nleads):
            ens_ts = mod_da.sel(iteration=l).isel(L=lvals+i).mean('L').rename({'Y':'time'})
            ens_time_year = mod_time.isel(L=lvals+i).mean('L').data
            ens_ts = ens_ts.assign_coords(time=("time",ens_time_year))
            a,b = xr.align(ens_ts,obs_ts)
            b = b - b.mean('time')
            if detrend:
                a = detrend_linear(a,'time')
                b = detrend_linear(b,'time')
            amean = a.mean('M')
            sigobs = b.std('time')
            sigsig = amean.std('time')
            if (resamp>0):
                iterations = resamp
                ens_size = 1
                a_resamp = xs.resample_iterations_idx(a, iterations, 'M', dim_max=ens_size).squeeze()
                sigtot = a_resamp.std('time').mean('iteration')
            else:
                sigtot = a.std('time').mean('M')
            r = xs.pearson_r(amean,b,dim='time')
            rpc = r/(sigsig/sigtot)
            corr_list.append(r)
            rpc_list.append(rpc.where(r>0))
            rmse_list.append(xs.rmse(amean,b,dim='time')/sigobs)
            msss_list.append(1-(xs.mse(amean,b,dim='time')/b.var('time')))
            pval_list.append(xs.pearson_r_eff_p_value(amean,b,dim='time'))
            sigsig_list.append(sigsig)
            sigtot_list.append(sigtot)
            s2t_list.append(sigsig/sigtot)
        corr = xr.concat(corr_list,lvalsda)
        pval = xr.concat(pval_list,lvalsda)
        rmse = xr.concat(rmse_list,lvalsda)
        msss = xr.concat(msss_list,lvalsda)
        rpc = xr.concat(rpc_list,lvalsda)
        sigs = xr.concat(sigsig_list,lvalsda)
        sigt = xr.concat(sigtot_list,lvalsda)
        s2t  = xr.concat(s2t_list,lvalsda)
        dslist.append(xr.Dataset({'corr':corr,'pval':pval,'rmse':rmse,'msss':msss,'rpc':rpc,'sig_sig':sigs,'sig_tot':sigt,'s2t':s2t}))
    dsout = xr.concat(dslist,dim='iteration')
    if (mean):
        dsout = dsout.mean('iteration')
    return dsout

def compute_resampskill_seasonal(mod_da,mod_time,obs_da,climy0,climy1,nleadavg=1,nleads=1,detrend=False,resamp=0,mean=True):
    """
    Computes a suite of skill scores for annual data. Includes option to use xskillscore resampling to
    compute the mean variance of individual member time series ("sigma_total").
    Assumes mod_time and obs_da.time both contain year values.
    """
    dslist = []
    lvals = np.arange(nleadavg)*4
    # Convert to leadtime values
    lvalsda = xr.DataArray(mod_da.isel(L=slice(0,nleads)).L-2,dims="L",name="L")
    
    for l in mod_da.iteration.values:
        corr_list = []; pval_list = []; rmse_list = []; msss_list = []; rpc_list = []
        sigobs_list = []; sigsig_list = []; sigtot_list = []; s2t_list = []
        for i in range(nleads):
            leadisel = lvals + i 
            ens_ts = mod_da.sel(iteration=l).isel(L=leadisel).mean('L').rename({'Y':'time'})
            ens_time_year = mod_time.isel(L=leadisel).mean('L').dt.year
            ens_time_month = mod_time.isel(L=leadisel).mean('L').dt.month.data[0]
            ens_ts = ens_ts.assign_coords(time=("time",ens_time_year.data))
            obsisel = obs_da.time.dt.month==ens_time_month
            obs_seas = obs_da.isel(time=obsisel)
            obs_seas = obs_seas - obs_seas.sel(time=slice(climy0,climy1)).mean('time')
            obs_seas = obs_seas.assign_coords(time=("time",obs_seas.time.dt.year.data))
            if (nleadavg>1):
                obs_seas = obs_seas.rolling(time=nleadavg,min_periods=nleadavg, center=True).mean().dropna('time',how='all')
            a,b = xr.align(ens_ts,obs_seas)
            if detrend:
                a = detrend_linear(a,'time')
                b = detrend_linear(b,'time')
            amean = a.mean('M')
            sigobs = b.std('time')
            sigsig = amean.std('time')
            if (resamp>0):
                iterations = resamp
                ens_size = 1
                a_resamp = xs.resample_iterations_idx(a, iterations, 'M', dim_max=ens_size).squeeze()
                sigtot = a_resamp.std('time').mean('iteration')
            else:
                sigtot = a.std('time').mean('M')
            r = xs.pearson_r(amean,b,dim='time')
            rpc = r/(sigsig/sigtot)
            corr_list.append(r)
            rpc_list.append(rpc.where(r>0))
            rmse_list.append(xs.rmse(amean,b,dim='time')/sigobs)
            msss_list.append(1-(xs.mse(amean,b,dim='time')/b.var('time')))
            pval_list.append(xs.pearson_r_eff_p_value(amean,b,dim='time'))
            sigobs_list.append(sigobs)
            sigsig_list.append(sigsig)
            sigtot_list.append(sigtot)
            s2t_list.append(sigsig/sigtot)
        corr = xr.concat(corr_list,lvalsda)
        pval = xr.concat(pval_list,lvalsda)
        rmse = xr.concat(rmse_list,lvalsda)
        msss = xr.concat(msss_list,lvalsda)
        rpc = xr.concat(rpc_list,lvalsda)
        sigo = xr.concat(sigobs_list,lvalsda)
        sigs = xr.concat(sigsig_list,lvalsda)
        sigt = xr.concat(sigtot_list,lvalsda)
        s2t  = xr.concat(s2t_list,lvalsda)
        dslist.append(xr.Dataset({'corr':corr,'pval':pval,'rmse':rmse,'msss':msss,'rpc':rpc,'sig_sig':sigs,'sig_tot':sigt,'s2t':s2t}))
    dsout = xr.concat(dslist,dim='iteration')
    if (mean):
        dsout = dsout.mean('iteration')
    return dsout



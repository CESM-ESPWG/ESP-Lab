Preprocessors are applied to individual time series files in order to return mean CAM fields with centered time coordinates.

The main steps in preprocessing are:
1) Extract a time slice of size "nlead"
2) Create a lead time coordinate "L" that is an integer sequence
3) Swap "time" with "L" so that L becomes a shared coordinate to aggregate data over, while "time" becomes a data variable that will now have a "Y" dimension (hindcast start time)
4) Extract only the chosen "field" from the data file (together with the new "time" variable)
5) Chunk to include all "L" values (which all come from a single NetCDF file)

The default preprocessor is described in [data_access.preprocessor()](https://esp-lab.readthedocs.io/en/latest/data_access.html#data_access.preprocessor).

However, the preprocessor can be adapted for a number of cases, such as to return a [seasonal mean field](https://github.com/NCAR/SMYLE-analysis/blob/main/notebooks/SMYLE_overview_GMD_2022/compute_SMYLE_zooC_skill.ipynb) or [POP SST](https://github.com/NCAR/SMYLE-analysis/blob/main/notebooks/SMYLE_overview_GMD_2022/Fig05_regionalSST_ACC_RMSE.ipynb). A few examples of different kinds of preprocessors are available on the [tutorial page](https://esp-lab.readthedocs.io/en/latest/tutorials/index.html).

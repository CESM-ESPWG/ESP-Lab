Preprocessors are applied to individual time series files in order to return mean CAM fields with centered time coordinates.

The default preprocessor is described in [data_access.preprocessor()](https://esp-lab.readthedocs.io/en/latest/data_access.html#data_access.preprocessor).

However, the preprocessor can be adapted for a number of cases, such as to return a [seasonal mean field](https://github.com/NCAR/SMYLE-analysis/blob/main/notebooks/SMYLE_overview_GMD_2022/compute_SMYLE_zooC_skill.ipynb) or [POP SST](https://github.com/NCAR/SMYLE-analysis/blob/main/notebooks/SMYLE_overview_GMD_2022/Fig05_regionalSST_ACC_RMSE.ipynb).

A few examples of different kinds of preprocessors are available on the [tutorial page](https://esp-lab.readthedocs.io/en/latest/tutorials/index.html).

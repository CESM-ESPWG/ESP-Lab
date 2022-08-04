# Changelog

## Version 0.0 - March 25, 2022
Original version of code from Steve Yeager

## Version 0.1 - April 28, 2022
Updates have been made to include docstrings and comments, add readthedocs, adjust directory structure, improve hard coded sections of the code, clarify parameters, make functions directly accessible in `__init__.py`

## Version 1.0 - June 2, 2022
Updates include module documentation, testing capabilities, and various package setup requirements. ReadTheDocs and sphinx automodules have been implemented and include some FAQs, installation documentation, changelogs, and a how-to guide. Codecov has been implemented and testing increased from 0% to 42%. Continuous Integration and workflow requirements were updated.

## Version 1.1 - Aug 4, 2022
Stats.py has been updated to include new skill score wrapper functions, allowing users to compute annual and seasonal skill with data arrays that have or have not been resampled. Dependabot features have been added. Documentation was updated. Parameters have been adjusted in data_access.get_monthly_data() to include a list of years instead of start/end year. Package updates were made to avoid dask incompatabilities and generally update packages. Jupyter notebook examples were provided as a tutorial for users.


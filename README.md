========
Tablizer
========


.. image:: https://img.shields.io/pypi/v/tablizer.svg
        :target: https://pypi.python.org/pypi/tablizer

.. image:: https://img.shields.io/travis/robertson-mark/tablizer.svg
        :target: https://travis-ci.org/robertson-mark/tablizer

.. image:: https://readthedocs.org/projects/tablizer/badge/?version=latest
        :target: https://tablizer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Simple statistical summaries on DataFrames and arrays to SQL or sqlite database.


* Free software: CC0 1.0
* Documentation: https://tablizer.readthedocs.io.


Features
--------

Example use:

```

from tablizer.tablizer import calculate, store, get_existing_records
from tablizer.inputs import Inputs
import numpy as np
import pandas as pd
import netCDF4 as nc

value = 'air_temp'
input_path = '/data/albedo/tuolumne/ops/wy2019/ops/data/data20181001/smrfOutputs/air_temp.nc'
database = 'sqlite'
location  = '/home/markrobertson/wkspace/tablizer.db'
methods = ['mean','max','std','percentile']
run_name = 'test'
basin_id = 1
run_id = 1

# get input data
ncf = nc.Dataset(input_path)
arrays = ncf[value][:]
dates = ncf.variables['time'][:]
date_units = ncf.variables['time'].units
ncf.close()


for n in range(0,len(arrays[:,0,0])):
    date = nc.num2date(dates[n],date_units)
    array = arrays[n,:,:]

    # calculate simple statistics
    results = calculate(array, date, methods)

    # put on database
    store(results, value, database, location, run_name, basin_id, run_id, date)

# to get existing records
records = get_existing_records(location, database)

```

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

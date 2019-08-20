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

# initialize
array = np.array([[1,1,1,1], [np.nan,2,3,6]])
location  = '/<path>/tablizer.db'
methods = ['nanmean','nanmax','nanstd','nanpercentile']
value = 'air_temp'
date = pd.to_datetime('2019-8-18 23:00')
run_name = 'test'
basin_id = 1
run_id = 1

# calculate results
results = calculate(array, date, methods)

# put on database
store(results, value, location, run_name, basin_id, run_id, date)

# get existing records
records = get_existing_records(location)

```

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

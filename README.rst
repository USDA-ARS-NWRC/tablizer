=====
Tablizer
=====

=====
Features
=====

Example use:

.. code :: python
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

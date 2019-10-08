## Tablizer
[![GitHub version](https://badge.fury.io/gh/USDA-ARS-NWRC%2Ftablizer.svg)](https://badge.fury.io/gh/USDA-ARS-NWRC%2Ftablizer)
[![Build Status](https://travis-ci.org/USDA-ARS-NWRC/tablizer.svg?branch=devel)](https://travis-ci.org/USDA-ARS-NWRC/tablizer)

Tablizer calculates simple summary statistics for 2D arrays, and stores those results in a database.

#### Example Use

```
from tablizer.tablizer import summarize, store, get_existing_records
import numpy as np
from datetime import datetime
import os

date = datetime(2019,1,1,23,0,0)
value = 'thermal'
database = 'sqlite'
run_name = 'test'
basins = {'Tuolumne': {'watershed_id': 1, 'basin_id': 2}}
bid = basins['Tuolumne']['basin_id']
rid = 1
location = os.path.abspath('tablizer.db')
array = np.array([[1,1,1,1],[np.nan,2,3,6]])
methods = ['nanmean', 'std', 'nanpercentile']
percentiles = [25, 75]

# Make summary calculations
results = summarize(array, date, methods, [percentiles[0],percentiles[1]], 3)

# Place results on a database
store(results, value, database, location, run_name, bid, rid, date)

# Pull records from database
records = get_existing_records(location, database)

```

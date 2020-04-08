# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from tablizer.inputs import Inputs, Base
from tablizer.defaults import Units, Methods, Fields
from tablizer.tools import create_sqlite_database, check_inputs_table, insert, \
    make_session, check_existing_records, delete_records, make_cnx_string


def summarize(array, date, methods, percentiles=[25, 75], decimals=3,
              masks=None, mask_zero_values=False):
    """
    Calculate basic summary statistics for 2D arrays or DataFrames.

    Args
    ------
    array {arr}: 2D array or DataFrame
    date {str}: ('2019-8-18 23:00'), anything pd.to_datetime() can parse
    methods {list}: (['mean','std']), strings of numpy functions to apply
    percentiles {list}: ([low, high]), must supply when using 'percentile'
    decimals {int}: rounding
    masks {list}: mask outputs
    mask_zero_values {bool}: mask zero values in array

    Returns
    ------
    result {DataFrame}: index = date, columns = methods
    """

    method_options = Methods.options

    if not isinstance(methods, list):
        raise TypeError("methods must be a list")

    if type(array) not in [np.ndarray, pd.core.frame.DataFrame]:
        raise Exception('array type {} not valid'.format(type(array)))

    if len(array.shape) != 2:
        raise Exception('array must be 2D array or DataFrame')

    if type(array) == pd.core.frame.DataFrame:
        array = array.values

    try:
        date_time = pd.to_datetime(date)
    except ValueError:
        print('pandas.to_datetime() failed with -> {}'.format(date))

    # check methods and create columns list
    cols = [x for x in methods if 'percentile' not in x]

    for method in methods:
        if method not in method_options:
            raise Exception('Method must be in {}'.format(method_options))

        if 'percentile' in method:
            if type(percentiles) != list:
                raise Exception('percentiles must be a list')

            if type(percentiles[0]) != int or type(percentiles[1]) != int:
                raise Exception('percentiles must be list of int')

            if len(percentiles) != 2 or (percentiles[1] < percentiles[0]):
                raise Exception('percentiles must [low, high]')

            cols = cols + ['{}_{}'.format(method, str(percentiles[0])),
                           '{}_{}'.format(method, str(percentiles[1]))]

    result = pd.DataFrame(index=[date_time], columns=cols)

    if masks is not None:
        if type(masks) != list:
            masks = [masks]

        for idx, mask in enumerate(masks):

            if mask.shape != array.shape:
                raise Exception('mask dimensions {} must match array '
                                'dimensions '
                                '{}'.format(mask.shape, array.shape))

            if mask_zero_values:
                ixz = array == 0
                array[ixz] = np.nan

            mask = mask.astype('float')
            mask[mask < 1] = np.nan
            array = array * mask

    for col, method in zip(cols, methods):

        if 'percentile' in method:
            c1 = '{}_{}'.format(method, str(percentiles[0]))
            c2 = '{}_{}'.format(method, str(percentiles[1]))
            v = getattr(np, method)(array, [percentiles[0], percentiles[1]])

            if not np.isnan(v).any():
                v = v.round(decimals)
                result.loc[date_time, c1] = v[0]
                result.loc[date_time, c2] = v[1]

            else:
                result.loc[date_time, c1] = np.nan
                result.loc[date_time, c2] = np.nan

        else:
            v = getattr(np, method)(array)

            if not np.isnan(v):
                v = v.round(decimals)
                result.loc[date_time, col] = v

    return result


def store(values, variable, database, location, run_name, basin_id, run_id,
          date_time, overwrite=True, units=None):
    '''

    Args
    ------
    values : pd.DataFrame, index = date_time, columns = methods
    variable : str ('air_temp')
    database : str, options are 'sql' or 'sqlite'
    location : str
        mysql database: user:pwd@host/database
        sqlite database: /<path>/database.db
    run_name : str
    basin_id : dict
    run_id : int
    date_time : datetime
    overwrite : bool, overwrite existing records if they exist
    units : dict, default supplied by defaults.py, check there for format

    '''

    if type(variable) != str:
        raise Exception('id must be type string')

    if len(variable) > 30:
        raise Exception('id string must be < 30 characters')

    if type(values) != pd.core.frame.DataFrame:
        raise Exception('values must be pandas.DataFrame')

    if database not in ['sql', 'sqlite']:
        raise Exception('database must be "sql" or "sqlite"')

    if type(run_name) != str:
        raise Exception('run_name must be type string')

    if type(run_id) != int:
        raise Exception('run_id must be type int')

    if type(basin_id) != int:
        raise Exception('basin_id must be type int')

    if units is None:
        units = Units.units

    location = make_cnx_string(location, database)

    fields = Fields.fields

    # create if it doesn't exist
    if database == 'sqlite':

        if not os.path.isfile(location):
            create_sqlite_database(location)

        # check if inputs table exists
        flag = check_inputs_table(location)

        if not flag:
            engine = create_engine(location)
            Base.metadata.create_all(engine, tables=[Inputs.__table__])

        date = pd.Timestamp(np.datetime64(values.index.values[0])).to_pydatetime()

        flag = check_existing_records(location, run_name, basin_id, date, variable)

        if overwrite and flag:
            delete_records(location, run_name, basin_id, date, variable)

        for v in values:
            fields['run_id'] = run_id
            fields['basin_id'] = basin_id
            fields['run_name'] = run_name
            fields['date_time'] = date_time
            fields['variable'] = variable
            fields['function'] = v
            fields['value'] = values[v].values
            fields['unit'] = units[variable]

            insert(location, 'Inputs', fields)

        return

    if database == 'sql':

        # check if inputs table exists
        flag = check_inputs_table(location)

        if not flag:
            engine = create_engine(location)
            Base.metadata.create_all(engine, tables=[Inputs.__table__])

        date = pd.Timestamp(np.datetime64(values.index.values[0])).to_pydatetime()

        flag = check_existing_records(location, run_name, basin_id, date, variable)

        if overwrite and flag:
            delete_records(location, run_name, basin_id, date, variable)

        for v in values:
            fields['run_id'] = run_id
            fields['basin_id'] = basin_id
            fields['run_name'] = run_name
            fields['date_time'] = date_time
            fields['variable'] = variable
            fields['function'] = v
            fields['value'] = values[v].values
            fields['unit'] = units[variable]

            insert(location, 'Inputs', fields)


def get_existing_records(location, database, query_dict=None):
    '''
    Get existing database records.

    Args
    ------
    location : str
        mysql database example: user:pwd@host/database
        sqlite database example: /<path>/database.db
    database : str, options are 'sql' or 'sqlite'
    query_dict : dict, if None default will be
        {'Inputs':['run_id','run_name','basin_id']}
        For existing database records will query {table:['field1','field2']}

    Returns
    ------
    results : dict {field:value}

    '''

    if database not in ['sql', 'sqlite']:
        raise Exception('database must be "sql" or "sqlite"')

    if query_dict is None:
        query_dict = {'Inputs': ['run_id', 'run_name', 'basin_id']}

    location = make_cnx_string(location, database)

    session = make_session(location)

    for k in query_dict.keys():
        qry = session.query(Inputs)
        results = pd.read_sql(qry.statement, qry.session.connection())

    session.close()

    return results

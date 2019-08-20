# -*- coding: utf-8 -*-

from tablizer.inputs import Inputs, Base
from tablizer.defaults import Units, Methods, Items
from tablizer.tools import create_sqlite_database, check_inputs_table, insert, make_session, check_existing_records, delete_records
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def calculate(input, date, methods, percentiles = [25,75], decimals = 3):
    '''
    Calculate basic summary statistics for 2D arrays or DataFrames.

    Args
    ------
    input : 2D array or DataFrame
    date : str ('2019-8-18 23:00'), anything pd.to_datetime() can parse
    methods : list (['mean','std']), strings of numpy functions to apply
    percentiles : list ([low, high]), must supply when using 'percentile'
    decimals : int

    Returns
    ------
    result : pd.DataFrame, index = date, columns = methods

    '''

    method_options = Methods.options

    if type(methods) != list:
        methods = [methods]

    if type(input) not in [np.ndarray, pd.core.frame.DataFrame]:
        raise Exception('input type {} not valid'.format(type(input)))

    if len(input.shape) != 2:
        raise Exception('input must be 2D array or DataFrame')

    if type(input) == pd.core.frame.DataFrame:
        input = input.values

    try:
        date_time = pd.to_datetime(date)

    except:
        raise Exception('unable to parse {} with pd.to_datetime()'.format(date))

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

            cols = cols + ['{}_{}'.format(method,str(percentiles[0])),
                           '{}_{}'.format(method,str(percentiles[1]))]

    result = pd.DataFrame(index = [date_time], columns = cols)

    for col, method in zip(cols, methods):

        if 'percentile' in method:
            c1 = '{}_{}'.format(method,str(percentiles[0]))
            c2 = '{}_{}'.format(method,str(percentiles[1]))
            v = getattr(np, method)(input,[percentiles[0],percentiles[1]])
            v = v.round(decimals)
            result.loc[date_time,c1] = v[0]
            result.loc[date_time,c2] = v[1]

        else:
            v = getattr(np, method)(input)
            v = v.round(decimals)
            result.loc[date_time,col] = v

    return result

def get_existing_records(location, query_dict = None):
    '''
    Get existing database records.

    Args
    ------
    location : str
    query_dict : dict, if None default will be
        {'Inputs':['run_id','run_name','basin_id']}
        For existing database records will query {table:['field1','field2']}

    Returns
    ------
    results : dict {field:value}

    '''

    if query_dict is None:
        query_dict = {'Inputs':['run_id','run_name','basin_id']}

    session = make_session(location)

    results = {}
    for k in query_dict.keys():
        qry = session.query(Inputs)
        df = pd.read_sql(qry.statement, qry.session.connection())
        results[k] = df

    session.close()

    return results

def store(values, variable, location, run_name, basin_id, run_id, date_time,
          overwrite = True, credentials = None, units = None):
    '''

    pd.Timestamp(np.datetime64(values.index.values[0])).to_pydatetime()

    Args
    ------
    values : pd.DataFrame, index = date_time, columns = methods
    variable : str ('air_temp')
    location : str
        mysql database: user:pwd@host:port/database
        sqlite database: /<path>/database.db
    run_name : str
    run_id : int
    date_time : datetime
    basin_id : int
    overwrite : bool, overwrite existing records if they exist
    credentials : dict {'user':username,'pwd':pwd} if using mysql
    units : dict, default supplied by defaults.py, check there for format

    '''

    # check variable
    if type(variable) != str:
        raise Exception('id must be type string')

    if len(variable) > 30:
        raise Exception('id string must be < 30 characters')

    # check values
    if type(values) != pd.core.frame.DataFrame:
        raise Exception('values must be pandas.DataFrame')

    # very basic location check
    ext = os.path.splitext(location)[1]

    if ext not in ['.db', '']:
        raise Exception('location string not valid')

    if units is None:
        units = Units.units

    if type(run_name) != str:
        raise Exception('run_name must be type string')

    if type(run_id) != int:
        try:
            run_id = int(run_id)
        except:
            raise Exception('run_id must be type int')

    if type(basin_id) != int:
        try:
            basin_id = int(basin_id)
        except:
            raise Exception('basin_id must be type int')

    items = Items.items

    # save to sqlite database
    if ext == '.db':

        # create if it doesn't exist
        if not os.path.isfile(location):
            create_sqlite_database(location)

        # check if inputs table exists
        flag = check_inputs_table(location)

        if not flag:
            print('create table here')

        date = pd.Timestamp(np.datetime64(values.index.values[0])).to_pydatetime()

        flag = check_existing_records(location, run_name, basin_id, date, variable)

        if overwrite and flag:
            delete_records(location, run_name, basin_id, date, variable)

        for v in values:
            items['run_id'] = run_id
            items['basin_id'] = basin_id
            items['run_name'] = run_name
            items['date_time'] = date_time
            items['variable'] = variable
            items['function'] = v
            items['value'] = values[v].values
            items['unit'] = units[variable]

            insert(location, 'Inputs', items)

        return

    # if mysql:
    #       # check credentials
    #
    #       # check table
    #
    #       # place results
    #
    #     return

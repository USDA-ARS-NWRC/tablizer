
from sqlalchemy import create_engine, and_
from tablizer.inputs import Inputs, Base
import tablizer
import pandas as pd
import numpy as np
import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tablizer.defaults import Units, Fields

def make_cnx_string(location, database):
    '''
    Make a connection string for sqlalchemy for either sql or sqlite.

    Args
    ------
    location : str
    database : str, either 'sql' or 'sqlite'

    Returns
    ------
    location : str, amended location string for sqlalchemy

    '''

    if database not in ['sql','sqlite']:
        raise Exception('database must be "sql" or "sqlite"')

    if database == 'sqlite':
        if 'sqlite:///' not in location:
            location = 'sqlite:///' + location

    if database == 'sql':
        if 'mysql+mysqlconnector://' not in location:
            location = 'mysql+mysqlconnector://' + location

    return location

def make_session(location):
    '''
    Make database session for sqlalchemy for either mysql or sqlite database.

    Args
    ------
    location : str

    Returns
    ------
    session : object, database session

    '''

    try:
        engine = create_engine(location)
        Base.metadata.create_all(engine)

    except:
        raise Exception('Failed to make database connection with '
                        '{}'.format(location))

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session

def create_sqlite_database(location):
    '''
    Create simple sqlite database.

    Args
    ------
    location : str, absolute path to database ending in .db

    '''

    engine = create_engine(location)
    Base.metadata.create_all(engine)

def check_inputs_table(location):
    '''
    Check that inputs table exists.

    Args
    ------
    location : str, absolute path to database ending in .db

    Returns
    ------
    flag : bool

    '''

    flag = False

    engine = create_engine(location)

    if engine.dialect.has_table(engine,'Inputs'):
        flag = True

    return flag

def insert(location, table, values):
    '''
    Inserts results in database.

    Args
    --------
    location : str, database connection
    table : str ('Inputs'), database table
    values : dict, {'run_id':run_id,
                    'run_name':run_name,
                    'basin_id':basin_id,
                    'date_time':datetime,
                    'variable':variable,
                    'function':function,
                    'value': value,
                    'unit': unit}

    '''

    fields = Fields.fields.keys()

    # check values
    for k in fields:
        if k not in values.keys():
            raise Exception('values must contain "{0}":{0}'.format(k))

    session = make_session(location)

    for val in values['value']:

        if np.isnan(val):
            val = None
        else:
            val = float(val)

        output = {'run_id': int(values['run_id']),
                  'run_name': values['run_name'],
                  'basin_id': int(values['basin_id']),
                  'date_time': values['date_time'],
                  'variable': values['variable'],
                  'function':values['function'],
                  'value': val,
                  'unit': values['unit']}

        dbtable = getattr(tablizer.inputs, table)
        my_dbtable = dbtable()

        for k,v in output.items():
            setattr(my_dbtable, k, v)

        session.add(my_dbtable)
        session.commit()

    session.close()

def check_existing_records(location, run_name, basin_id, date_time, variable):
    '''
    Check if there are existing records on the Inputs table.

    Args
    ------
    location : str
    run_name : str
    basin_id : int
    date_time : datetime
    variable : str

    Returns
    ------
    flag : bool

    '''
    flag = False

    session = make_session(location)

    qry = session.query(Inputs).filter(and_((Inputs.run_name == run_name),
                                            (Inputs.basin_id == basin_id),
                                            (Inputs.date_time == date_time),
                                            (Inputs.variable == variable)))

    df = pd.read_sql(qry.statement, qry.session.connection())

    if not df.empty:
        flag = True

    return flag

def delete_records(location, run_name, basin_id, date_time, variable):
    '''
    Delete existing records from Inputs table.

    Any records with matching run_name, basin_id, date_time, and variable will
    be deleted.

    Args
    ------
    location : str
    run_name : str
    basin_id : int
    date_time : datetime
    variable : str

    '''

    session = make_session(location)
    session.query(Inputs).filter(and_((Inputs.run_name == run_name),
                                      (Inputs.basin_id == basin_id),
                                      (Inputs.date_time == date_time),
                                      (Inputs.variable == variable))).delete()
    session.flush()
    session.commit()
    session.close()

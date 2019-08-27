
class Units():
    units = {'air_temp':'C',
             'cloud_factor':'none',
             'net_solar': 'W/m^2',
             'percent_snow': '%',
             'precip': 'mm',
             'snow_density': 'kg/m^3',
             'storm_days': 'day',
             'thermal': 'W/m^2',
             'vapor_pressure': 'pascal',
             'wind_speed': 'm/s^2'}

class Methods():
    options = ['nanmean','nanmin','nanmax','nanstd','nanpercentile', 'nanstd',
               'mean','min','max','std','percentile', 'median', 'nanmedian']

class Fields():
    fields = {'run_id': '',
             'basin_id': '',
             'run_name': '',
             'date_time': '',
             'variable': '',
             'function': '',
             'value': '',
             'unit': ''}

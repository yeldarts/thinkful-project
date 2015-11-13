import time
from dateutil.parser import parse
import collections
import sqlite3 as lite
import requests
from pandas.io.json import json_normalize
import datetime
import pandas as pd
import matplotlib.pyplot as plt

con = lite.connect('citi_bike.db')
cur = con.cursor()
cur.execute('DELETE FROM available_bikes')

for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', ((exec_time-datetime.datetime(1970,1,1)).total_seconds(),))
    con.commit()

    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + str((exec_time-datetime.datetime(1970,1,1)).total_seconds()) + ";")
    con.commit()

    time.sleep(60)

con.close() #close the database connection when done
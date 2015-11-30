import os, sys
import time
from dateutil.parser import parse
import collections
import sqlite3 as lite
import requests
from pandas.io.json import json_normalize
import datetime
import pandas as pd
import matplotlib.pyplot as plt

#cities = { "Atlanta": '33.762909,-84.422675'}
cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
colors = {"Atlanta": 'b',
            "Austin": 'g',
            "Boston": 'r',
            "Chicago": 'c',
            "Cleveland": 'm'
        }

        
apiKey = 'ef157c4f6c94a5a31c0ffdfc2da3cf50'

print datetime.datetime.now()

inputMissing = 1
userInput = raw_input("Recreate the database (Y or N)?")

if (os.path.isfile('weather.db') and userInput == 'Y'):
    os.remove('weather.db')
con = lite.connect('weather.db')
cur = con.cursor()

if userInput == 'Y':
    
    #create the static table that holds the different cities
    with con:
        cur.execute("""CREATE TABLE cities 
                        (cityid INT PRIMARY KEY,
                         city TEXT, 
                         location TEXT )""")
                      
    #create the dynamic table that holds the different temps
    with con:
        cur.execute("""CREATE TABLE temps 
                        (dateunix INT,
                         cityid INT, 
                         maxtemp REAL,
                         PRIMARY KEY (dateunix, cityid) )""")
    
                         
    #a prepared SQL statement we're going to execute over and over again
    citySql = """INSERT INTO cities 
               (cityid, 
                city, 
                location) 
                VALUES (?,?,?)"""
                
    #a prepared SQL statement we're going to execute over and over again
    tempSql = """INSERT INTO temps 
               (dateunix, 
                cityid, 
                maxtemp) 
                VALUES (?,?,?)"""
                
    cityID = 1
    #https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME
    for key in cities:
        print key, 'corresponds to', cities[key]
        #Insert the city into the database
        with con:
            cur.execute(citySql,(cityID,
                             key,
                             cities[key]))
        for dayCounter in range(30):
            startDate = datetime.datetime.now() - datetime.timedelta(days=dayCounter)
            startUnix = int((startDate-datetime.datetime(1970,1,1)).total_seconds())
            print startDate
            print startUnix
            #Handle the API call
            apiCall = 'https://api.forecast.io/forecast/' + apiKey + '/' + cities[key] + ',' + str(startUnix)
            #print apiCall
            r = requests.get(apiCall)
            #print "both keys"
            #print r.json().keys()
            
            #print "daily"
            #print r.json()['daily']
            #print "data"
            #print r.json()['daily']['data']
            #print "temperatureMax"
            #print r.json()['daily']['data'][0]['temperatureMax']
            
            with con:
                cur.execute(tempSql,(startUnix,
                                 cityID,
                                 r.json()['daily']['data'][0]['temperatureMax']))
        cityID += 1


print "Starting to deal with the plots"

cur.execute("""SELECT cityid, city
                 FROM cities""")
cityList = cur.fetchall()
for cityid, city in cityList:
    print "city " + city
    print "cityid " + str(cityid)
    cur.execute("""select maxtemp
                   from temps 
                   where cityid = """ + str(cityid) + """
                   order by dateunix""")
    temps = cur.fetchall()
    plt.plot(range(30), temps, colors[city], label=city)
plt.legend()
plt.show()
import os, sys
from bs4 import BeautifulSoup
import requests
import sqlite3 as lite

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)

if (os.path.isfile('web_scrape.db')):
    os.remove('web_scrape.db')
con = lite.connect('web_scrape.db')
cur = con.cursor()

with con:
    cur.execute("""CREATE TABLE countries 
                    (country TEXT PRIMARY KEY,
                     year INT,
                     men INT, 
                     women INT )""")
    cur.execute("""create table gdp 
                   (country_name text, 
                    _1999 real, 
                    _2000 real, 
                    _2001 real, 
                    _2002 real, 
                    _2003 real, 
                    _2004 real, 
                    _2005 real, 
                    _2006 real, 
                    _2007 real, 
                    _2008 real, 
                    _2009 real, 
                    _2010 real)""")
                     
dbInsert = """INSERT INTO countries 
               (country, 
                year, 
                men,
                women) 
                VALUES (?,?,?,?)"""
#for row in soup('table'):
#    print(row)
    
print "table 9"
print type(soup('table')[9])
print soup('table')[9].name
print soup('table')[9].attrs
    
print "rows time"
rows = soup('table')[9].find_all("tr")

for row in rows:

    for key in row.attrs:
        print key, 'corresponds to', row.attrs[key]
        if row.attrs[key][0] == 'tcont':
            print "use it"
            cells = row.find_all("td")
            print "country: ", cells[0].get_text()
            print "year: ", cells[1].get_text()
            print "total: ", cells[4].get_text()
            print "men: ", cells[7].get_text()
            print "women: ", cells[10].get_text()
            with con:
                cur.execute(dbInsert,(cells[0].get_text(),
                    cells[1].get_text(),
                    cells[7].get_text(),
                    cells[10].get_text()))

import csv

with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv','rU') as inputFile:
    next(inputFile) # skip the first two lines
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    print header[44]
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        print line[0]
        with con:
            cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[43:-6]) + '");')                             
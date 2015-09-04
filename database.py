import sqlite3 as lite
import pandas as pd

cities = (('Las Vegas', 'NV'),
          ('Atlanta', 'GA'),
          ('New York City', 'NY'),
          ('Boston', 'MA'),
          ('Chicago', 'IL'),
          ('Miami', 'FL'),
          ('Dallas', 'TX'),
          ('Seattle', 'WA'),
          ('Portland', 'OR'),
          ('San Francisco', 'CA'),
          ('Los Angeles', 'CA'))

weather = (('Las Vegas', 2013, 'July', 'December',''),
           ('Atlanta', 2013, 'July', 'January',''),
           ('New York City',2013,'July','January',62),
           ('Boston',2013,'July','January',59),
           ('Chicago',2013,'July','January',59),
           ('Miami',2013,'August','January',84),
           ('Dallas',2013,'July','January',77),
           ('Seattle',2013,'July','January',61),
           ('Portland',2013,'July','December',63),
           ('San Francisco',2013,'September','December',64),
           ('Los Angeles',2013,'September','December',75))

con = lite.connect('getting_started.db')


with con:

    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS cities')
    cur.execute('CREATE TABLE cities (name text, state text)')
    cur.execute('DROP TABLE IF EXISTS weather')
    cur.execute('CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)')
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)
    
    #cur.execute("SELECT * FROM cities")
    #print "starting rows"
    #rows = cur.fetchall()
    #for row in rows:
    #    print row
    #cols = [desc[0] for desc in cur.description]
    #df = pd.DataFrame(rows, columns=cols)
    #print "starting headers"
    #headers = df.columns.values.tolist()
    #for header in headers:
    #    print header
  
    inputMissing = 1
    userInput = raw_input("What month do you want to limit to?")
    while(inputMissing):
        if(userInput != ''):
            inputMissing = 0
        else:
            userInput = raw_input("Please enter a month")
    
        
      
    cur.execute("""SELECT c.name, c.state
                   FROM cities c
                   LEFT JOIN weather w on (c.name = w.city)
                  WHERE upper(w.warm_month) = '""" + userInput.upper() + "'")
    rows = cur.fetchall()
    #for row in rows:
    #    print row
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    headers = df.columns.values.tolist()
    #for header in headers:
    #    print header
    cityList = ''
    cityCount = 1
    for row_index, row in df.iterrows():
        if (cityCount > 1):
            cityList += '; '
        cityList += row[0] + ', ' + row[1]
        cityCount += 1
    
    if(cityList == ''):
        print 'No cities are warmest in ' + userInput
    else:
        print 'The cities that are warmest in ' + userInput + ' are: ' + cityList
    
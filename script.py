import psycopg2
from geopy import *

con = psycopg2.connect(database="dwik", user="postgres",
                       password="mddwikabdro", host="localhost", port="5432")

geolocator = Nominatim(user_agent="week7")
cur = con.cursor()
cur.execute('''SELECT retrieve_addresses();''')
addresses = cur.fetchall()

cur.execute('''alter table address add column longitude float;''')
cur.execute('''alter table address add column latitude float;''')

con.commit()

for item in addresses:
    location = geolocator.geocode(item[0])
    latitude = 0
    longitude = 0
    if location!=None:
        latitude = location.latitude
        longitude = location.longitude
    cur.execute('''UPDATE address 
                    SET latitude = '''+str(latitude)+''', 
                    longitude = '''+str(longitude)+''' 
                    WHERE address.address=\''''+item[0]+'''\';''')
    con.commit()


con.close()

import numpy as np
import random
import datetime
import mysql.connector
import time
# imported all essential libraries

# specifying the number of users/phone numbers to be generated
samples = 100

# specifying the number of the data points per user to be generated
data_points = 100

# declaring a counter variable
counter = 0

# connecting to the database
print("Connecting to the database...")
cnx = mysql.connector.connect(
    host="",
    port=3306,
    user='',
    password="",
    db="phone_data")

print("Connected to the database...")

# initializing cursor
cur = cnx.cursor()
cur.execute("truncate table phone_gps")

print("Updating the database")
print("This might take a while...")

# generating 10 phone numbers
for i in range(samples):
    print(i)
    phone = str(random.randint(6000000000, 9999999999))
    # generating 5 coordinates
    h = 0
    m = 0
    s = 0
    for j in range(data_points):
        print("\t %d" % (j))
        lat = random.uniform(i+21.1463, i+21.14675)
        lon = random.uniform(i+79.0849, i+79.0854)
        x = datetime.datetime.now()
#        print("x=",x)
        str1 = x.isoformat()
        s += 1
        if s == 60:
            s = 0
            m += 1
            if m == 60:
                m = 0
                h += 1
                if h == 24:
                    h = 0
        s1 = str(s).zfill(2)
        m1 = str(m).zfill(2)
        h1 = str(h).zfill(2)
        tim = str1[:10] + " " + h1 + ":" + m1 + ":" + s1 + str1[19:]
        # inserting to the database table
        # actual query would be "insert into phone_gps values(phone,lat,lon,tim,"null",primary_key)"
        cur.execute("insert into phone_gps values(" +
                    "'" + phone + "'" +
                    "," + str(lat) +
                    "," + str(lon) +
                    "," + "'" + str(tim) + "'" +
                    ", null," + str(counter) + ")")
        counter += 1


# committing the changes
cnx.commit()

# closing the database connection
cnx.close()

print("The changes have been updated successfully!")

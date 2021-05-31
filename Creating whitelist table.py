import mysql.connector
from random import randint

# declaring a counter variable
counter = 0

# number of samples you want to print
samples = 10

# connection to the database
print("Connecting to the database...")
cnx = mysql.connector.connect(
    host="",
    port=3306,
    user="",
    password="",
    db="phone_data")
print("Connected to the database...")

# setting cursor for the database
cur = cnx.cursor()

# deleting contents of table
cur.execute("truncate table whitelist")

# selecting each unique phone number
cur.execute("select distinct phone_no from phone_gps")

phone_list = cur.fetchall()

# to update the reason column
reas = ["Police", "Paramedic", "Fire", "Health Inspector", "Military"]

print("Updating the database")
print("This might take a while...")
for i in range(samples):
    print(i)
    phone = phone_list[i][0]
    counter += 1
    j = randint(0, 4)
    cur.execute("insert into whitelist values("+"'"+phone +
                "'"+","+str(counter)+","+"'"+reas[j]+"'"+")")

cnx.commit()

cnx.close()

print("The database has been updated successfully!")

import mysql.connector

# setting counter variable
counter = 0

# number of users you want to generate
samples = 5

# connecting to the database
print("Connecting to the database...")

cnx = mysql.connector.connect(
    host="",
    port=3306,
    user="",
    password="",
    db="phone_data"
)

print("Connected to the database...")

# setting the cursor for the table
cur = cnx.cursor()

# truncating existing values
cur.execute("truncate table repeater_check")

# generating a list of distinct phone numbers from phone_gps
cur.execute("select distinct phone_no from phone_gps")
phone_list = cur.fetchall()

# inserting into table
print("Updating the database")
print("This may take a while...")
for i in range(samples):
    print(i+1)
    phone_no = phone_list[i][0]
    cur.execute("insert into repeater_check values(" +
                phone_no+","+str(counter)+")")
    counter += 1

# committing the changes to the table
cnx.commit()

# closing the connection
cnx.close()
print("The database has been updated successfully!")

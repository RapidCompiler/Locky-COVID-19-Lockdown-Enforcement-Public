from sklearn.cluster import KMeans
import mysql.connector
from dbConnect import connect
import numpy as np
import matplotlib.pyplot as plt

'''
INPUT PARAMETERS. CONVERT THIS SECTION TO OBTAIN THESE INPUTS FROM A USER INTERFACE
MODIFY THESE PARAMETERS AS NEEDED
'''

# Tolerance Distance in metres
tolerance_distance = 20

# Percentage of entries that can violate the distance rule
tolerance_violations = 0.34

# Number of most recent locations to check for violations
tolerance_recency = 2

'''
K-MEANS CLUSTERING ALGORITHM.
'''


def isViolator(points):
    kmeans = KMeans(n_clusters=1, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    pred_y = kmeans.fit_predict(points)
    violations = []
    for i in range(len(points)):
        if (((points[i][0] - kmeans.cluster_centers_[0][0])**2 + (points[i][1] - kmeans.cluster_centers_[0][1])**2)**0.5) * 100000 > tolerance_distance:
            violations.append(1)
        else:
            violations.append(0)
    violator = []
    if violations.count(1) / len(points) > tolerance_violations:  # Proximity Rule Violation
        violator.append(True)
    else:
        violator.append(False)
    # Recency Rule Violation
    if violations[tolerance_recency*-1:].count(1) > 0:
        violator.append(True)
    else:
        violator.append(False)
    return violator


'''
MAIN PROCESSING
'''

'''
THIS ENSURES SUCCESSFUL CONNECTION TO THE MySQL DATABASE. PLEASE EDIT THIS PART TO READ DATA FROM ANY OTHER DATABASE
'''
cnx = connect()

# Setting the cursor
cur = cnx.cursor()

# Ignoring phone numbers that are in the Whitelist table
cur.execute(
    "select distinct phone_no from phone_gps where phone_no not in (select phone_no from whitelist)")
req_phone_list = cur.fetchall()
print("There are totally", len(req_phone_list),
      "phone numbers that need to be processed...")

count = 0
for phone_no in range(len(req_phone_list)):
    cur.execute("select latitude, longitude from phone_gps where phone_no =" +
                req_phone_list[phone_no][0])
    data = cur.fetchall()
    points = np.ndarray(shape=(len(data), 2), dtype=float)
    x = 0
    for row in data:
        points[x][0] = row[0]
        points[x][1] = row[1]
        x += 1
    check = isViolator(points)
    if check[0] or check[1]:
        print("User", req_phone_list[phone_no][0], "is a VIOLATOR")
        count += 1
    else:
        print("User", req_phone_list[phone_no][0], "is NOT a VIOLATOR")
    if check[0] and check[1]:
        # Update repeater_table for further processing
        cur.execute("insert into repeater_table (phone_no, count) values (" +
                    req_phone_list[phone_no][0] + "," + str(1) + ") on duplicate key update count = count + 1")

print("There are", count, "violators out of", len(req_phone_list))

'''
ADD SPECIFIC LOGIC BELOW, FOR APPROPRIATE HANDLING OF VIOLATORS. ALL PHONE NUMBERS HAVE BEEN ADDED TO THE TABLE NAMED "repeater_table" IN THE SAME DATABASE IN MySQL
'''

cnx.commit()

cnx.close()

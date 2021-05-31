# Locky : COVID-19-Lockdown-Enforcement using python AI

Locky uses KMeans AI Clustering Algorithm to plot the coordinates of a user's location, determine the cluster center and identify outliers (When the user goes outside a certain radius from the center)

This repository contains all the programs required in order to make the main program "Locky - Golden" function correctly. The files "dbConnect" and "python_mysql_dbconfig" ensure successful connection to the MySQL database. Change those files accordingly if needed.

This project requires a config.ini file containing the details given below.

[mysql]

host = localhost

database = database_name

user = username

password =password

In this example, the database name is "phone_data". If the config.ini file is then added to the same repository, the program will read data from MySQL databases, which will need to be created and populated on the computer in which this program is being executed. All parameters will need to changed sufficiently.

A full comprehensive report of this project can be found on my website [here](https://sanjaysuresh.com/Project/portal/project_details_locky.html)

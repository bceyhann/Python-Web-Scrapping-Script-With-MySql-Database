import mysql.connector
from mysql_connector_conf import host_url, user_id, user_pass

db = mysql.connector.connect(
    host=host_url,
    user=user_id,
    passwd=user_pass
)

cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE scrapper")
    print("TABLE SUCCESFULLY CREATED!")
except:
    print("DB ALREADY EXIST...")

db = mysql.connector.connect(
    host=host_url,
    user=user_id,
    passwd=user_pass,
    database="scrapper"
)

cursor = db.cursor()

try:
    cursor.execute("CREATE TABLE vulnlab (ID int NOT NULL AUTO_INCREMENT, DATE NVARCHAR(20), ADVISORYNAME NVARCHAR(100), VERSION NVARCHAR(5), TYPE VARCHAR(100), AUTHOR NVARCHAR(100), LINKLIST NVARCHAR(100), CATHEGORY VARCHAR(100), PRIMARY KEY (ID))")
    print("TABLE SUCCESFULLY CREATED, ALL FINISHED!")
except:
    print("TABLE ALREADY EXIST... ALL FINISHED!")


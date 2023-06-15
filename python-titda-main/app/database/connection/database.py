import mysql.connector
from mysql.connector import errorcode

db_host = '31.220.56.44'
db_user = 'root'
db_password = 'password'
db_name = 'moodle'
cnx = 0

try:
    cnx = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

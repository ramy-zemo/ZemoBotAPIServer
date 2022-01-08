import mysql.connector
from config import DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE

# Databse Setup
conn_main = mysql.connector.connect(
    host=DB_IP,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE,
    auth_plugin='mysql_native_password'
)
cur_main = conn_main.cursor(buffered=True)

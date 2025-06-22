import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

config = {
  'user': os.getenv("user"),
  'password': os.getenv("password"),
  'host': os.getenv("host"),
  'database': os.getenv("database")
}

def connect_to_mysql():
    try:
        return mysql.connector.connect(**config)
    except (mysql.connector.Error, IOError) as err:
        print("Failed to connect, exiting without a connection: %s", err)
        return None        
    
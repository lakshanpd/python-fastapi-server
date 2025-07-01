from dotenv import load_dotenv
import os
import mysql.connector
from models import User
from errors import DatabaseError
from datetime import datetime, timezone

load_dotenv()

add_user_query = "INSERT INTO user (id, first_name, last_name, birthday, email, phone_number, created_at, updated_at, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" 
get_email_query = "SELECT email FROM user WHERE email = %s"
get_password_query = "SELECT password FROM user WHERE email = %s"
get_user_claims_query = "SELECT id, first_name, last_name, email, created_at, updated_at FROM user WHERE email = %s"

config = {
  'user': os.getenv("user"),
  'password': os.getenv("password"),
  'host': os.getenv("host"),
  'database': os.getenv("database")
}

class SqlHandler:
    def __init__(self):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()
    
    def add_user_to_db(self, user: User):
        try:
            cursor = self.connection.cursor()
            user_data = (str(user.id), user.first_name, user.last_name, user.birthday, user.email, user.phone_number, user.updated_at, user.created_at, user.password)
            cursor.execute(add_user_query, user_data)
            self.connection.commit()
        except Exception:
            raise DatabaseError("Error while adding user to db")
            
    # if a record with the given email exists returns true, otherwise false  
    def check_email_exist(self, email: str):
        try:
            self.cursor.execute(get_email_query, (email,))
            result = self.cursor.fetchall()
            if len(result) > 0:
                return True 
            return False
        except Exception:
            raise DatabaseError("Error while adding user to db")
        
    # get hashed password from database for given email  
    def get_hashed_password(self, email):
        try:
            self.cursor.execute(get_password_query, (email,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception:
            raise DatabaseError("Error while fetching user password to match")
        
    # get user claims from database for given email  
    def get_user_claims(self, email):
        try:
            self.cursor.execute(get_user_claims_query, (email,))
            result = self.cursor.fetchone()
            access_token_claims = {
                "iss": "python-fastapi-server",
                "aud": "python-fastapi-server",
                "type": "access_token",
                "id": result[0],
                "first name": result[1],
                "last name": result[2],
                "email": result[3],
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int(datetime.now(timezone.utc).timestamp()) + 3600 # expiration time is one hour
            }
            refresh_token_claims = {
                "iss": "python-fastapi-server",
                "aud": "python-fastapi-server",
                "type": "refresh_token",
                "email": result[3],
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int(datetime.now(timezone.utc).timestamp()) + 604800 # expiration time is one week
            }
            return [access_token_claims, refresh_token_claims]
        except Exception:
            raise DatabaseError("Error while fetching user claims")
        
sql_handler = SqlHandler()

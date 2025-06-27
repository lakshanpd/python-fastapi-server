from models import User
from .connection import connect_to_mysql
from .queries import add_user_query, get_email_query, get_password_query, get_user_claims_query
from errors import DatabaseError
from datetime import datetime, timezone

def add_user_to_db(user: User):
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            user_data = (str(user.id), user.first_name, user.last_name, user.birthday, user.email, user.phone_number, user.updated_at, user.created_at, user.password)
            cursor.execute(add_user_query, user_data)
            connection.commit()
        except Exception as error:
            raise DatabaseError("Error while adding user to db")
          
# if a record with the given email exists returns true, otherwise false  
def check_email_exist(email: str):
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(get_email_query, (email,))
            result = cursor.fetchall()
            if len(result) > 0:
                return True 
            return False
        except Exception as error:
            raise DatabaseError("Error while adding user to db")
      
# get hashed password from database for given email  
def get_hashed_password(email):
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(get_password_query, (email,))
            result = cursor.fetchone()
            return result[0]
        except Exception as error:
            raise DatabaseError("Error while fetching user password to match")
        
# get user claims from database for given email  
def get_user_claims(email):
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(get_user_claims_query, (email,))
            result = cursor.fetchone()
            access_token_claims = {
                "iss": "python-fastapi-server",
                "aud": "python-fastapi-server",
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
                "email": result[3],
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int(datetime.now(timezone.utc).timestamp()) + 604800 # expiration time is one week
            }
            return [access_token_claims, refresh_token_claims]
        except Exception as error:
            raise DatabaseError("Error while fetching user claims")
        
        
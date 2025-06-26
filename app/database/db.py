from models import User
from .connection import connect_to_mysql
from .queries import add_user_query, get_email_query, get_password_query
from errors import DatabaseError

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
        
        
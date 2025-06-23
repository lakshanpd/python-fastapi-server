from app.models.index import User
from datetime import date, datetime
from .connection import connect_to_mysql
from .queries import add_user

def user_registration(user: User):
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            user_data = (user.id, user.first_name, user.last_name, user.birthday, user.email, user.phone_number, user.updated_at, user.created_at)
            cursor.execute(add_user, user_data)
            connection.commit()
            print("Record added successfully.")
        except Exception as error:
            print("Error while user registration: ", error)
        finally:
            return
    
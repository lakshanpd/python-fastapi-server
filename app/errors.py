# Custom exception for errors related to database operations
class DatabaseError(Exception):
    pass

# Custom exception for errors during user registration process
class UserRegistrationError(Exception):
    pass

# Custom exception for invalid data type errors
class InvalidTypeError(Exception):
    pass

# Custom exception for errors during user login process
class UserLoginError(Exception):
    pass

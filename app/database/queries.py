add_user_query = "INSERT INTO user (id, first_name, last_name, birthday, email, phone_number, created_at, updated_at, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" 
get_email_query = "SELECT email FROM user WHERE email = %s"
get_password_query = "SELECT password FROM user WHERE email = %s"
get_user_claims_query = "SELECT id, first_name, last_name, email, created_at, updated_at FROM user WHERE email = %s"
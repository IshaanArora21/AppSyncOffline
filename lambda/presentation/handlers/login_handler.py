from ..db_details import build_response,close_db_connection,get_db_connection
from http import HTTPStatus
import bcrypt
import jwt
import datetime

secret_key='secretKey'
def handle_login(event_arguments):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        email = event_arguments["user"]["email"]
        password = event_arguments["user"]["password"]

        cursor.execute("SELECT id, guid, first_name, last_name, email, password FROM \"user\" WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            id, guid, first_name, last_name, email_db, hashed_password = user
            
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                payload = {
                    "id": id,
                    "guid": guid,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email_db,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  
                }
                
                
                jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
                print(jwt_token)
               
                result = {
                    "id": id,
                    "guid": guid,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email_db,
                    "jwt_token": jwt_token
                }
                
                return build_response(HTTPStatus.OK, result)
            else:
                return build_response(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
        else:
            return build_response(HTTPStatus.UNAUTHORIZED, "Invalid credentials")

    finally:
        cursor.close()
        close_db_connection(connection)

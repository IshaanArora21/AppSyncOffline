import jwt
from ..db_details import build_response
from http import HTTPStatus

secret_key = 'secretKey'

def handle_authenticateUser(event_arguments):
    token = event_arguments["jwt_token"]

    jwt_token = jwt.decode(token, secret_key, algorithms=["HS256"])

    user_credentials = {
        "id": jwt_token["id"],
        "guid": jwt_token["guid"],
        "first_name": jwt_token["first_name"],
        "last_name": jwt_token["last_name"],
        "email": jwt_token["email"],
        "jwt_token": token
    }

    return build_response(HTTPStatus.OK, user_credentials)
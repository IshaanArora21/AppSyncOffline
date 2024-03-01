import json
import psycopg2
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "WalkIn"
DB_USER = "postgres"
DB_PASSWORD = "Ishaan1908###"
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return connection


def close_db_connection(connection):
    if connection:
        connection.close()


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body, default=str),
        "headers": {"Content-Type": "application/json"},
    }


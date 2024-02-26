import json
import uuid
import psycopg2
import datetime
from http import HTTPStatus

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


def handle_graphql(event, context):
    event = json.loads(event["body"])

    data = []
    print("hello")
    if type(event) == list:
        for each_event in event:
            data.append(handle_each_request(each_event))
    else:
        data = handle_each_request(event)

    return data


def handle_each_request(event):
    field_name = event["info"]["fieldName"]
    event_source = event["source"]
    event_arguments = event["arguments"]

    data = []

    if field_name == "getAllWalkInDrives":
        connection = get_db_connection()
        try:
            cursor = connection.cursor()

            drive_query = """
                            SELECT id, guid, drive_title, dt_created, dt_modified, start_date, end_date, location
                            FROM walk_in_drive
                        """
            job_title_query = """
                                SELECT jr.job_title,jr.package,jr.job_description,job_requirements
                                FROM job_role jr
                                JOIN drive_job_role_mapping dhjr ON jr.id = dhjr.job_role_id
                                WHERE dhjr.drive_id = %s
                            """
            time_slot_query = """
                                SELECT ts.slot_timings
                                FROM timeslot ts
                                JOIN drive_timeslot_mapping dhts ON ts.id = dhts.timeslot_id
                                WHERE dhts.drive_id = %s
                                """

            cursor.execute(drive_query)
            drives = cursor.fetchall()
            cursor.close()

            results = []

            for drive in drives:
                drive_id = drive[0]

                cursor = connection.cursor()
                cursor.execute(job_title_query, (drive_id,))
                job_details = []

                for row in cursor.fetchall():
                    job_details.append({
                        'job_title': row[0],
                        'package': row[1],
                        'job_description': row[2],
                        'job_requirements': row[3]
                    })
                cursor.execute(time_slot_query, (drive_id,))
                time_slots = [row[0] for row in cursor.fetchall()]
                cursor.close()
                result = {
                    'id': drive[0],
                    'guid': drive[1],
                    'drive_title': drive[2],
                    'dt_created': drive[3],
                    'dt_modified': drive[4],
                    'start_date': drive[5],
                    'end_date': drive[6],
                    'location': drive[7],
                    'job_Roles': job_details,
                    'time_Slots': time_slots
                }
                results.append(result)

            for result in results:
                print(result)

            cursor.close()
            return build_response(HTTPStatus.OK, results)

        finally:
            cursor.close()
            close_db_connection(connection)

    if field_name == "getAllUsers":
        connection = get_db_connection()
        try:
            cursor = connection.cursor()

            drive_query = """
                            SELECT * FROM "user"
                        """

            cursor.execute(drive_query)
            result2 = cursor.fetchall()
            cursor.close()

            results = []

            results = [
                {
                    "id": row[0],
                    "guid": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "email": row[4],
                    "password": row[5],
                    "phone_no": row[6],
                    "resume": row[7],
                    "portfolio_url": row[8],
                    "profile_pic": row[9],
                    "dt_created": str(row[10]),
                    "dt_modified": str(row[11]),
                }
                for row in result2
            ]
            for result in results:
                print(result)

            cursor.close()
            return build_response(HTTPStatus.OK, results)

        finally:
            cursor.close()
            close_db_connection(connection)

    if field_name == "getWalkInDriveByGUID":
        connection = get_db_connection()
        try:
            cursor = connection.cursor()

            drive_guid = event_arguments["guid"]
            print(drive_guid)

            drive_query = """
                            SELECT id, guid, drive_title, dt_created, dt_modified, start_date, end_date, location
                            FROM walk_in_drive
                            WHERE guid = %s
                          """
            job_title_query = """
                                SELECT jr.job_title, jr.package, jr.job_description, job_requirements
                                FROM job_role jr
                                JOIN drive_job_role_mapping dhjr ON jr.id = dhjr.job_role_id
                                WHERE dhjr.drive_id = %s
                              """
            time_slot_query = """
                                SELECT ts.slot_timings
                                FROM timeslot ts
                                JOIN drive_timeslot_mapping dhts ON ts.id = dhts.timeslot_id
                                WHERE dhts.drive_id = %s
                              """

            cursor.execute(drive_query, (drive_guid,))
            drive = cursor.fetchone()
            print(drive)

            if drive:
                drive_id = drive[0]

                cursor.execute(job_title_query, (drive_id,))
                job_details = []

                for row in cursor.fetchall():
                    job_details.append({
                        'job_title': row[0],
                        'package': row[1],
                        'job_description': row[2],
                        'job_requirements': row[3]
                    })
                cursor.execute(time_slot_query, (drive_id,))
                time_slots = [row[0] for row in cursor.fetchall()]

                result = {
                    'id': drive[0],
                    'guid': drive[1],
                    'drive_title': drive[2],
                    'dt_created': drive[3],
                    'dt_modified': drive[4],
                    'start_date': drive[5],
                    'end_date': drive[6],
                    'location': drive[7],
                    'job_Roles': job_details,
                    'time_Slots': time_slots
                }
                results = [result]
                print(results)
                return build_response(HTTPStatus.OK, results[0])

        finally:
            cursor.close()
            close_db_connection(connection)

    if field_name == "getUserByGUID":
        connection = get_db_connection()
        try:
            cursor = connection.cursor()

            user_guid = event_arguments["guid"]

            user_query = """
                            SELECT * FROM "user" WHERE guid = %s
                         """

            cursor.execute(user_query, (user_guid,))
            user = cursor.fetchone()

            if user:
                result = {
                    "id": user[0],
                    "guid": user[1],
                    "first_name": user[2],
                    "last_name": user[3],
                    "email": user[4],
                    "password": user[5],
                    "phone_no": user[6],
                    "resume": user[7],
                    "portfolio_url": user[8],
                    "profile_pic": user[9],
                    "dt_created": str(user[10]),
                    "dt_modified": str(user[11]),
                }
                results = [result]
                print(results)
                return build_response(HTTPStatus.OK, results[0])

        finally:
            cursor.close()
            close_db_connection(connection)



    

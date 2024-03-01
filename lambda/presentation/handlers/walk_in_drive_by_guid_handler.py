from ..db_details import build_response,close_db_connection,get_db_connection
from http import HTTPStatus
def handle_get_walk_in_drive_by_guid(event_arguments):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        drive_guid = event_arguments["guid"]

        drive_query = """
                        SELECT id, guid, drive_title, dt_created, dt_modified, start_date, end_date, location,
                               general_instructions, instructions_for_exam, minimum_system_requirements, process, expiry
                        FROM walk_in_drive
                        WHERE guid = %s
                      """
        job_title_query = """
                            SELECT jr.id, jr.job_title, jr.package, jr.job_description, job_requirements
                            FROM job_role jr
                            JOIN drive_job_role_mapping dhjr ON jr.id = dhjr.job_role_id
                            WHERE dhjr.drive_id = %s
                          """
        time_slot_query = """
                            SELECT ts.id, ts.slot_timings
                            FROM timeslot ts
                            JOIN drive_timeslot_mapping dhts ON ts.id = dhts.timeslot_id
                            WHERE dhts.drive_id = %s
                          """

        cursor.execute(drive_query, (drive_guid,))
        drive = cursor.fetchone()

        if drive:
            drive_id = drive[0]

            cursor.execute(job_title_query, (drive_id,))
            job_details = []

            for row in cursor.fetchall():
                job_details.append({
                    'id': row[0],
                    'job_title': row[1],
                    'package': row[2],
                    'job_description': row[3],
                    'job_requirements': row[4]
                })

            cursor.execute(time_slot_query, (drive_id,))
            time_slots = [{'id': row[0], 'slot_timings': row[1]} for row in cursor.fetchall()]

            result = {
                'id': drive[0],
                'guid': drive[1],
                'drive_title': drive[2],
                'dt_created': drive[3],
                'dt_modified': drive[4],
                'start_date': drive[5],
                'end_date': drive[6],
                'location': drive[7],
                'general_instructions': drive[8],
                'instructions_for_exam': drive[9],
                'minimum_system_requirements': drive[10],
                'process': drive[11],
                'expiry': drive[12],  # Expiry field added
                'job_Roles': job_details,
                'time_Slots': time_slots
            }
            results = [result]
            return build_response(HTTPStatus.OK, results[0])

    finally:
        cursor.close()
        close_db_connection(connection)

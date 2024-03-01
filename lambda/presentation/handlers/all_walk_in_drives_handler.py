
from ..db_details import build_response,close_db_connection,get_db_connection
from http import HTTPStatus

def handle_get_all_walk_in_drives(event_arguments):
    connection = get_db_connection()
    cursor = None  # Initialize cursor outside the try block
    try:
        cursor = connection.cursor()

        drive_query = """
                        SELECT wd.id, wd.guid, wd.drive_title, wd.dt_created, wd.dt_modified,
                               wd.start_date, wd.end_date, wd.location, wd.expiry,
                               wd.general_instructions, wd.instructions_for_exam,
                               wd.minimum_system_requirements, wd.process
                        FROM walk_in_drive wd
                    """
        cursor.execute(drive_query)
        drives = cursor.fetchall()

        results = []

        for drive in drives:
            drive_id = drive[0]

            # Fetch job details for each drive
            job_query = """
                            SELECT jr.id, jr.job_title, jr.package, jr.job_description, jr.job_requirements
                            FROM job_role jr
                            JOIN drive_job_role_mapping dhjr ON jr.id = dhjr.job_role_id
                            WHERE dhjr.drive_id = %s
                        """
            cursor.execute(job_query, (drive_id,))
            job_details = []
            for row in cursor.fetchall():
                job_details.append({
                    'id': row[0],
                    'job_title': row[1],
                    'package': row[2],
                    'job_description': row[3],
                    'job_requirements': row[4]
                })

            timeslot_query = """
                    SELECT ts.id, ts.slot_timings
                    FROM timeslot ts
                    JOIN drive_timeslot_mapping dtm ON ts.id = dtm.timeslot_id
                    WHERE dtm.drive_id = %s
                 """
            cursor.execute(timeslot_query, (drive_id,))
            timeslot_details = []
            for row in cursor.fetchall():
             timeslot_details.append({
               'id': row[0],
                'slot_timings': row[1]
            })


            # Add drive details to the results
            result = {
                'id': drive[0],
                'guid': drive[1],
                'drive_title': drive[2],
                'dt_created': drive[3],
                'dt_modified': drive[4],
                'start_date': drive[5],
                'end_date': drive[6],
                'location': drive[7],
                'expiry': drive[8],
                'general_instructions': drive[9],
                'instructions_for_exam': drive[10],
                'minimum_system_requirements': drive[11],
                'process': drive[12],
                'job_Roles': job_details,
                'time_Slots': timeslot_details
            }
            results.append(result)

        return build_response(HTTPStatus.OK, results)

    except Exception as e:
        print(f"Error fetching data: {e}")

    finally:
        if cursor:
            cursor.close()
        close_db_connection(connection)


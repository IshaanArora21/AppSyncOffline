from ..db_details import build_response, close_db_connection, get_db_connection
from http import HTTPStatus

def hallticket_handler(event_arguments):
    try:
        hallticket = event_arguments["hallticket"]
        user_id = hallticket["user_id"]
        job_role_id = hallticket["job_role_id"]
        walk_in_drive_id = hallticket["walk_in_drive_id"]
        timeslot_id = hallticket["timeslot_id"]
        
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch job title
        job_role_query = f"SELECT job_title FROM job_role WHERE id = {job_role_id}"
        cursor.execute(job_role_query)
        job_title = cursor.fetchone()
        job_title = job_title[0] if job_title else None

        # Fetch slot timings
        timeslot_query = f"SELECT slot_timings FROM timeslot WHERE id = {timeslot_id}"
        cursor.execute(timeslot_query)
        slot_timings = cursor.fetchone()
        slot_timings = slot_timings[0] if slot_timings else None

        # Fetch walk-in details
        walk_in_details_query = f"""
            SELECT id, company_name, address_line_1, area, pincode, 
                   things_to_remember, phone ,city,start_date
            FROM walk_in_drive 
            WHERE id = {walk_in_drive_id}
        """
        cursor.execute(walk_in_details_query)
        walk_in_details_row = cursor.fetchone()
        walk_in_details = {
            'id': walk_in_details_row[0],
            'company_name': walk_in_details_row[1],
            'address_line_1': walk_in_details_row[2],
            'area': walk_in_details_row[3],
            'pincode': walk_in_details_row[4],
            'things_to_remember': walk_in_details_row[5],
            'phone': walk_in_details_row[6],
            'city':walk_in_details_row[7],
            'start_date':walk_in_details_row[8]
        }

        hallticket_output = {
            'user_id': user_id,
            'slot_timings': slot_timings,
            'job_title': job_title,
            'walk_in_drive_id': walk_in_drive_id,
            'company_name': walk_in_details['company_name'],
            'address_line_1': walk_in_details['address_line_1'],
            'area': walk_in_details['area'],
            'pincode': walk_in_details['pincode'],
            'things_to_remember': walk_in_details['things_to_remember'],
            'phone': walk_in_details['phone'],
            'city': walk_in_details['city'],
            'start_date':walk_in_details['start_date']
        }

        return build_response(HTTPStatus.OK, hallticket_output)

    except Exception as e:
        response = build_response(HTTPStatus.INTERNAL_SERVER_ERROR, {'error': str(e)})
        return response

    finally:
        if cursor:
            cursor.close()
        close_db_connection(connection)



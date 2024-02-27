import json
import uuid
import psycopg2
import datetime
from http import HTTPStatus
from psycopg2.extras import execute_values
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
    event_arguments = event["arguments"]

    data = []

    if field_name == "getAllWalkInDrives":
        connection = get_db_connection()
        try:
            cursor = connection.cursor()

            drive_query = """
                            SELECT id, guid, drive_title, dt_created, dt_modified, start_date, end_date, location,expiry
                            FROM walk_in_drive
                        """
            job_title_query = """
                                SELECT jr.id,jr.job_title,jr.package,jr.job_description,job_requirements
                                FROM job_role jr
                                JOIN drive_job_role_mapping dhjr ON jr.id = dhjr.job_role_id
                                WHERE dhjr.drive_id = %s
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
                        'id':row[0],
                        'job_title': row[1],
                        'package': row[2],
                        'job_description': row[3],
                        'job_requirements': row[4]
                    })
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
                    'expiry':drive[8],
                    'job_Roles': job_details,
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

        drive_query = """
                        SELECT id, guid, drive_title, dt_created, dt_modified, start_date, end_date, location,
                               general_instructions, instructions_for_exam, minimum_system_requirements, process, expiry
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
    
    if field_name == "login":
     connection = get_db_connection()
     try:
        cursor = connection.cursor()

        email = event_arguments["user"]["email"]
        password = event_arguments["user"]["password"]
    
        query = """
            SELECT first_name, last_name, email FROM "user" WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            print("hello")
            first_name, last_name, email = user
            result = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
            print(result) 
            return build_response(HTTPStatus.OK, result)
     

   
     finally:
        cursor.close()
        close_db_connection(connection)

    if field_name == "applyDrive":
     connection = get_db_connection()
     try:
        cursor = connection.cursor()

        updated_resume = event_arguments["applicantInput"]["updated_resume"]
        walk_in_drive_id = event_arguments["applicantInput"]["walk_in_drive_id"]
        timeslot_id = event_arguments["applicantInput"]["timeslot_id"]
        user_id = event_arguments["applicantInput"]["user_id"]
        job_role_ids = event_arguments["applicantInput"]["job_role_id"]
        guid = str(uuid.uuid4())
        dt_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt_modified = dt_created

        applied_drive_query = """
            INSERT INTO applied_drive (guid, updated_resume, walk_in_drive_id, timeslot_id, user_id, dt_created, dt_modified)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        cursor.execute(applied_drive_query, (guid, updated_resume, walk_in_drive_id, timeslot_id, user_id, dt_created, dt_modified))
        applied_drive_id = cursor.fetchone()[0]

        applied_drive_job_role_query = """
            INSERT INTO applied_drive_job_role_mapping (applied_drive_id, job_role_id) VALUES (%s, %s)
        """
        for job_role_id in job_role_ids:
            cursor.execute(applied_drive_job_role_query, (applied_drive_id, job_role_id))

        location_query = """
            SELECT location FROM walk_in_drive WHERE id = %s
        """
        cursor.execute(location_query, (walk_in_drive_id,))
        location = cursor.fetchone()[0]

        current_date=datetime.date.today().strftime("%Y-%m-%d")
        
        timeslot_query = """
            SELECT slot_timings FROM timeslot WHERE id = %s
        """
        cursor.execute(timeslot_query, (timeslot_id,))
        timings = cursor.fetchone()[0]

        connection.commit()

        response_data = {
            "location": location,
            "date": current_date,
            "timings": timings
        }

        return build_response(HTTPStatus.OK, response_data)

     finally:
        cursor.close()
        close_db_connection(connection)

    if field_name == "createUser":
        print("Creating user...")

        personalInfo = event_arguments['newUser']['personalInfo']
        educationalQualification = event_arguments['newUser']['educationalQualification']
        professionalQualification = event_arguments['newUser']['professionalQualification']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            first_name = personalInfo['first_name']
            last_name = personalInfo['last_name']
            email = personalInfo['email']
            password = personalInfo['password']
            phone_no = personalInfo['phone_no']
            resume = personalInfo['resume']
            portfolio_url = personalInfo.get('portfolio_url', None)  
            profile_pic = personalInfo.get('profile_pic', None)  
            preferred_Job_roles_id = personalInfo['preferred_Job_roles_id']

            aggregate_percentage = educationalQualification['aggregate_percentage']
            passing_year = educationalQualification['passing_year']
            degree = educationalQualification['degree']
            stream = educationalQualification['stream']
            college = educationalQualification['college']
            college_city = educationalQualification['college_city']

            applicant_type = professionalQualification['applicant_type']
            applied_test = professionalQualification['applied_test']
            applied_test_role = professionalQualification.get('applied_test_role', None)  
            familiarTechnologies = professionalQualification['familiarTechnologies']
            experienced_qualification = professionalQualification.get('experienced_qualification', None)

        
            cursor.execute("""
                INSERT INTO "user" (first_name, last_name, email, password, phone_no, resume, portfolio_url, profile_pic)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (first_name, last_name, email, password, phone_no, resume, portfolio_url, profile_pic))

            user_id = cursor.fetchone()[0]
            print("User ID:", user_id)

           
            user_jobRole_data = [(user_id, job_role_id) for job_role_id in preferred_Job_roles_id]
            sql_user_has_job_role = """
                INSERT INTO user_job_role_mapping (user_id, job_role_id)
                VALUES %s
            """
            execute_values(cursor, sql_user_has_job_role, user_jobRole_data)

           
            cursor.execute("""
                INSERT INTO educational_qualification (user_id, aggregate_percentage, passing_year, degree, stream, college, college_city)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, aggregate_percentage, passing_year, degree, stream, college, college_city))

            
            experienced_qualification_id = None
            if experienced_qualification:
                print("Inserting data into experienced_qualification table...")
                experience_year = experienced_qualification['experience_year']
                current_ctc = experienced_qualification['current_ctc']
                expected_ctc = experienced_qualification['expected_ctc']
                notice_period = experienced_qualification['notice_period']
                notice_period_end = experienced_qualification['notice_period_end']
                notice_period_duration = experienced_qualification['notice_period_duration']

                cursor.execute("""
                    INSERT INTO experienced_qualification (experience_year, current_ctc, expected_ctc, notice_period, notice_period_end, notice_period_duration)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (experience_year, current_ctc, expected_ctc, notice_period, notice_period_end, notice_period_duration))

                experienced_qualification_id = cursor.fetchone()[0]

               
                expertiseTechnologies = experienced_qualification['expertiseTechnologies']
                expertise_technology_records = [(experienced_qualification_id, technology_id) for technology_id in expertiseTechnologies]
                sql_expertise_technology = """
                    INSERT INTO expertise_technology (experienced_qualification_id, technology_id)
                    VALUES %s
                """
                execute_values(cursor, sql_expertise_technology, expertise_technology_records)

            
            cursor.execute("""
                INSERT INTO professional_qualification (user_id, applicant_type, applied_test, applied_test_role, experienced_qualification_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, applicant_type, applied_test, applied_test_role, experienced_qualification_id))

            professional_qualification_id = cursor.fetchone()[0]

            
            familiarTechnologies_records = [(professional_qualification_id, technology_id) for technology_id in familiarTechnologies]
            sql_familiar_technology = """
                INSERT INTO familiar_technology (professional_qualification_id, technology_id)
                VALUES %s
            """
            execute_values(cursor, sql_familiar_technology, familiarTechnologies_records)

            connection.commit()
            results = {
                        "Registration successful"
                        }

            return build_response(HTTPStatus.OK, results)

        except Exception as e:
            print("Error inserting data:", e)
            connection.rollback()

        finally:
            cursor.close()
            close_db_connection(connection)

















    

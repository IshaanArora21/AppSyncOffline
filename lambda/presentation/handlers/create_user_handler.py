from ..db_details import build_response,close_db_connection,get_db_connection
from http import HTTPStatus
from psycopg2.extras import execute_values
import bcrypt
def handle_create_user(event_arguments):
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
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')
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
            """, (first_name, last_name, email, hashed_password_str, phone_no, resume, portfolio_url, profile_pic))

            user_id = cursor.fetchone()[0]
            print("User ID:", user_id)

           
            user_jobRole_data = [(user_id, job_role_id) for job_role_id in preferred_Job_roles_id]
            sql_user_has_job_role = """
                INSERT INTO user_job_role_mapping (user_id, job_role_id)
                VALUES %s
            """
            execute_values(cursor, sql_user_has_job_role, user_jobRole_data)

           
            cursor.execute("""
                INSERT INTO educational_qualifications (user_id, aggregate_percentage, passing_year, degree, stream, college, college_city)
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
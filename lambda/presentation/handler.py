import json
from .handlers.all_walk_in_drives_handler import handle_get_all_walk_in_drives
from .handlers.login_handler import handle_login
from .handlers.walk_in_drive_by_guid_handler import handle_get_walk_in_drive_by_guid
from .handlers.apply_drive_handler import handle_apply_drive
from .handlers.create_user_handler import handle_create_user
from .handlers.hallticket_handler import hallticket_handler
from .handlers.authenticateUser_handler import handle_authenticateUser
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

    if field_name == "getAllWalkInDrives":
        return handle_get_all_walk_in_drives(event_arguments)
        

    if field_name == "getWalkInDriveByGUID":
        return handle_get_walk_in_drive_by_guid(event_arguments)

    if field_name == "login":
     return handle_login(event_arguments)

    if field_name == "applyDrive":
     return handle_apply_drive(event_arguments)

    if field_name == "createUser":
     return handle_create_user(event_arguments)
        
    if field_name == "getHallTicket":
     return hallticket_handler(event_arguments)
    
    if field_name == 'authenticateUser':
       return handle_authenticateUser(event_arguments)

















    

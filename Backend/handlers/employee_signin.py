from datetime import datetime
from Backend.config.constants import db
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.handlers.login import handle_login


def handle_employee_signin(data):
    # Get the relevant data from the packet
    username = data['username']
    password = data['password']
    business_name = data['businessName']  # Modified from 'businessNumber'
    name = data['employeeName']

    # Access the relevant db controllers
    user_controller = UsersController(db)
    work_places_controller = WorkPlacesController(db)
    user_requests_controller = UserRequestsController(db)

    # Insert data into Users table
    user_data = {
        'username': username,
        'password': password,
        'name': name,
        'isManager': False,
        'isActive': True,
        'isApproval': False,
    }
    user_controller.create_entity(user_data)

    # Retrieve business ID based on business name
    business_id = work_places_controller.get_business_id_by_name(business_name)

    if business_id is None:
        # Handle the case where the business name is not found in the database
        return {"success": False, "message": "Business name not found"}

    # Insert data into workPlaces table
    work_place_data = {
        'workPlaceID': business_id,
        'id': user_controller.get_user_id_by_username_and_password(username, password)
    }
    work_places_controller.create_entity(work_place_data)

    # Insert data into userRequests table
    user_request_data = {
        'id': user_controller.get_user_id_by_username_and_password(username, password),
        'modifyAt': datetime.now(),
        'requests': '...'
    }
    user_requests_controller.create_entity(user_request_data)

    login_data = {"username": data["username"], "password": data["password"]}

    # Send the username and password to the login function to create a user session
    _, user_session = handle_login(login_data)  # Depends on the `handle_login` function to work properly.
    return user_session


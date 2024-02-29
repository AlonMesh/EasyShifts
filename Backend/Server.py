from __future__ import annotations
from enum import Enum
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController
from Backend.user_session import UserSession
from Backend.main import initialize_database_and_session
from Backend.db.models import ShiftPart
import websockets
import asyncio
import json
from datetime import datetime, timedelta
from Backend.handlers import login

# Initialize the database and session
db, _ = initialize_database_and_session()

# Global variable declaration
user_session: UserSession | None = None


class DayName(Enum):  # I moved this class over here cuz it's not supposed to be in the models file
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'


def handle_login(data):
    global user_session  # Declare user_session as a global variable

    # Access the username and password
    username = data['username']
    password = data['password']

    # Initialize the users controller, passing the database session
    users_controller = UsersController(db)

    # Check if the user exists and is a manager
    user_exists, is_manager = users_controller.check_user_existence_and_manager_status(username, password)

    if user_exists:
        # Retrieve the actual user ID from the database
        user_id = users_controller.get_user_id_by_username_and_password(username, password)

        # Create a UserSession object if the user exists
        user_session = UserSession(user_id=user_id, is_manager=is_manager)
    else:
        print("user doesnt exist!")
    # TODO: else: send a message to the client that the user does not exist

    # Return the pair of boolean values
    response = [user_exists, is_manager]
    return response


def handle_employee_signin(data):
    # Get the relevant data from the packet
    username = data['username']
    password = data['password']
    business_id = data['businessNumber']
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
    }
    user_controller.create_entity(user_data)

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
    handle_login(login_data)


def handle_manager_signin(data):
    """
    Handles the manager sign-up process by creating a new user using the UsersController.

    Parameters:
        data (dict): A dictionary containing user data for sign-up.
            Example: {'username': 'manager1', 'password': 'password123', 'name': 'Place Name'}

    Returns:
        dict: A dictionary containing the response to be sent back to the client.
            Example: {'success': True, 'message': 'Manager sign-up successful'}
    """
    try:
        print("IN")
        # Initialize the users controller
        user_controller = UsersController(db)

        # Insert the new manager into the database
        print(data)
        user_controller.create_entity(data)

        # Optionally, you can send a success response back to the client
        return {'success': True, 'message': 'Manager sign-up successful'}
    except Exception as e:
        # Handle any errors that occur during the sign-up process
        error_message = 'Error during manager sign-up: ' + str(e)
        print(error_message)
        return {'success': False, 'message': error_message}


def handle_employee_shifts_request(data):
    if user_session is None:
        print("User session not found.")
        return False
    user_id = user_session.get_id
    shifts_string = data.get('shiftsString')

    shifts_request_data = {"id": user_id, "modifyAt": datetime.now(), "requests": shifts_string}
    user_request_controller = UserRequestsController(db)
    user_request_controller.update_entity(user_id, shifts_request_data)


def handle_get_employee_requests(data):
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_id
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        if workplace_id is not None:
            # Assuming get_active_workers_for_user returns a list of active workers
            active_workers = work_places_controller.get_active_workers_for_user(user_id)
            employees_requests = {}
            user_requests_controller = UserRequestsController(db)
            for worker in active_workers:
                employees_requests[worker[1]] = user_requests_controller.get_request_by_userid(worker[0])

            return employees_requests

        else:
            print("User does not work in any workplace.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False


def handle_manager_insert_shifts(data):
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        shifts_controller = ShiftsController(db)
        shift_workers_controller = ShiftWorkersController(db)
        user_request_controller = UserRequestsController(db)
        users_controller = UsersController(db)
        employee_id = users_controller.get_user_id_by_username(data["username"])
        employee_request = user_request_controller.get_request_by_userid(employee_id)
        days = [DayName.Sunday, DayName.Monday, DayName.Tuesday, DayName.Wednesday, DayName.Thursday, DayName.Friday,
                DayName.Saturday]
        shift_parts = [ShiftPart.Morning, ShiftPart.Noon, ShiftPart.Evening]
        shifts = employee_request.split('_')
        for shift in shifts:
            shift_time, insert = shift.split('-')
            if insert == 't':
                part = 'm'
                if shift_time[1] == 'n':
                    part = shift_parts[1].value
                elif shift_time[1] == 'e':
                    part = shift_parts[2].value
                shift_id = shifts_controller.get_shift_id_by_day_and_part_and_workplace(
                    days[int(shift_time[0]) - 1].name, part, user_session.get_id)
                if shift_id is not None:
                    shift_worker = {'shiftID': shift_id, 'userID': employee_id}
                    shift_workers_controller.create_entity(shift_worker)

    else:
        print("User does not have access to manager-specific pages.")
        return False


def make_shifts():
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        shifts_controller = ShiftsController(db)
        current_date = datetime.now()
        next_sunday = current_date + timedelta(days=(6 - current_date.weekday() + 1) % 7)
        next_week_dates = [next_sunday + timedelta(days=i) for i in range(7)]
        shift_parts = [ShiftPart.Morning, ShiftPart.Noon, ShiftPart.Evening]
        days = [DayName.Sunday, DayName.Monday, DayName.Tuesday, DayName.Wednesday, DayName.Thursday, DayName.Friday,
                DayName.Saturday]
        for date in next_week_dates:
            for i in range(0, 3):
                shift = {"workPlaceID": user_session.get_id, "shiftDate": date.strftime("%Y-%m-%d"),
                         "shiftPart": shift_parts[i].value,
                         "shiftDay": days[datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d").weekday()].name}
                shifts_controller.create_entity(shift)

    else:
        print("User does not have access to manager-specific pages.")
        return False


def handle_employee_list():
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_id
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        if workplace_id is not None:
            # Assuming get_active_workers_for_user returns a list of active workers
            active_workers = work_places_controller.get_active_workers_for_user(user_id)

            # Convert list of tuples to a string
            active_workers_str = ' ,'.join(f'{worker[0]}: {worker[1]}' for worker in active_workers)

            return active_workers_str  # return active workers as a string
        else:
            print("User does not work in any workplace.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False


def handle_send_profile() -> dict:
    """
    Handles the request to send the user's profile data to the client.

    Returns:
        dict: A dictionary containing the user's profile data.
              The structure of the dictionary depends on the user's role (manager or worker).
    Raises:
        Exception: If the user session is not found.
    """
    if user_session is None:
        raise Exception("User session not found.")

    # Retrieve the user ID from the user session
    user_id = user_session.get_id

    # Initialize the users controller
    users_controller = UsersController(db)

    # Initialize the workplaces controller
    work_places_controller = WorkPlacesController(db)

    # Initialize the shifts controller
    shifts_controller = ShiftsController(db)

    # Create a dictionary to hold the returned data by key-value pairs
    returned_data = {
        "user_id": user_id,
        "username": users_controller.get_username_by_id(user_id)
    }

    # Retrieve the user's profile
    if user_session.can_access_manager_page():
        # Add manager-specific data to the dictionary
        returned_data["workplace_name"] = users_controller.get_name_by_id(user_id)  # name of manager = workplace name
        future_shifts = shifts_controller.get_future_shifts_for_workplace(user_id)  # user_id of manager = workplace_id
        future_shifts_for_client = convert_shifts_for_client(future_shifts, db)
        returned_data["future_shifts"] = future_shifts_for_client
    else:
        # Add worker-specific data to the dictionary
        returned_data["name"] = users_controller.get_name_by_id(user_id)
        returned_data["workplace_name"] = work_places_controller.get_workplace_name_by_worker_id(user_id)
        future_shifts = shifts_controller.get_future_shifts_for_user(user_id)
        future_shifts_for_client = convert_shifts_for_client(future_shifts, db, is_manager=False)
        returned_data["future_shifts"] = future_shifts_for_client

    # Return the dictionary
    return returned_data


def handle_request(request_id, data):
    global user_session
    if request_id == 10:
        # Login request handling
        print("Received Login request")
        print(data)

        response, user_session = login.handle_login(data)
        return response

    elif request_id == 20:
        # Employee Sign in request handling
        print("Received Employee Sign in request")
        handle_employee_signin(data)

    elif request_id == 30:
        # Manager Sign in request handling
        print("Received Manager Sign in request")
        handle_manager_signin(data)

    elif request_id == 40:
        # Employee's Shifts Request handling
        print("Received Employee's Shifts Request")
        handle_employee_shifts_request(data)

    elif request_id == 50:
        # Manager Get Employees Requests Request
        print("Received Manager Get Employees Requests Request")
        return handle_get_employee_requests(data)

    elif request_id == 55:
        # Manager Shifts inserting Request handling
        print("Received Manager Shifts inserting Request")
        handle_manager_insert_shifts(data)

    elif request_id == 60:
        # Employees list request handling
        print("Received Employees list request")
        return handle_employee_list()

    elif request_id == 70:
        # Employees list request handling
        print("Send user profile")
        profile_data = handle_send_profile()
        return {"request_id": request_id, "success": True, "data": profile_data}

    elif request_id == 80:
        # Make new week shifts
        print("Make new week shifts")
        make_shifts()

    else:
        print("Unknown request ID:", request_id)


async def handle_client(websocket, path):
    try:
        async for message in websocket:
            # Parse the JSON message
            data = json.loads(message)

            # Extract the request_id and data
            request_id = data.get('request_id', None)
            request_data = data.get('data', None)

            response = handle_request(request_id, request_data)
            json_data = json.dumps(response)
            await websocket.send(json_data)
            print(response)

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for {websocket.remote_address}")


async def start_server():
    try:
        db, _ = initialize_database_and_session()
        async with websockets.serve(handle_client, "localhost", 8080):
            print("Server started")
            await asyncio.Future()  # Keep the server running until Enter is pressed
    except asyncio.CancelledError:
        print("Server stopped.")
        exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


asyncio.run(start_server())

if __name__ == "__main__":
    asyncio.run(start_server())

from __future__ import annotations
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.user_session import UserSession
from Backend.main import initialize_database_and_session
import websockets
import asyncio
import json

# Initialize the database and session
db, _ = initialize_database_and_session()

# Initialize the user session. It's initially None until a user logs in
user_session: UserSession | None = None


def handle_login(data):
    global user_session  # Declare user_session as a global variable

    # Access the username and password
    username = data['username']
    password = data['password']

    # Initialize the users controller, passing the database session
    users_controller = UsersController(db)

    # Check if the user exists and is a manager
    user_exists, is_manager = users_controller.check_user_existence_and_manager_status(username, password)
    print(user_exists)
    print(is_manager)
    if user_exists:
        # Retrieve the actual user ID from the database
        user_id = users_controller.get_user_id_by_username_and_password(username, password)

        # Create a UserSession object if the user exists
        user_session = UserSession(user_id=user_id, is_manager=is_manager)

    # TODO: else: send a message to the client that the user does not exist

    # Return the pair of boolean values
    response = [user_exists, is_manager]
    return response


def handle_employee_signin(data):
    pass


def handle_manager_signin(data):
    """
    Handles the manager signin process by creating a new user using the UsersController.

    Parameters:
        data (dict): A dictionary containing user data for signin.
            Example: {'username': 'manager1', 'password': 'password123', 'isManager': True, 'isActive': True, 'name': 'Place Name'}
    """
    # TODO: Add a check to see if the user is already logged in. If so, return an error message to the client.

    # TODO: Add a check to see if the username already exists. If so, return an error message to the client.

    # TODO: Add a check to see if the workplace name already exists. If so, return an error message to the client.

    # TODO: Add a check to see if username is valid. If not, return an error message to the client.

    # TODO: Add a check to see if password is valid. If not, return an error message to the client.

    # Initialize the users controller, passing the database session
    user_controller = UsersController(db)
    user_controller.create_entity(data)

    # Send the username and password to the login function to create a user session
    login_data = {"username": data["username"], "password": data["password"]}
    handle_login(login_data)  # NEVER BEEN TESTED! Depends on the `handle_login` function to work properly.

    return None  # Should not return a response to the client


def handle_employee_shifts_request(data):
    user_id = user_session.get_id
    current_date = data.get('currentDate')
    shifts_string = data.get('shiftsString')
    shifts_request_data = {user_id, current_date, shifts_string}
    user_controller = UsersController(db)
    user_controller.create_entity(shifts_request_data)


def handle_manager_shifts(data):
    pass


def handle_employee_list():
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_id
        print(user_id)  # Works correctly to this point
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        print(workplace_id)  # Returns None
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


def get_request(msg):
    # Assuming the request ID is the first two bytes of the received data
    data = json.loads(msg)

    # Extract the request_id and data
    request_id = data.get('request_id', None)
    # Extract the rest of the data
    request_data = data.get('data', None)
    return request_id, request_data


def handle_request(request_id, data):
    if request_id == 10:
        # Login request handling
        print("Received Login request")
        print(data)

        response = handle_login(data)
        return response

    elif request_id == 20:
        # Employee Sign in request handling
        print("Received Employee Sign in request")
        print(data)
        handle_employee_signin(data)

    elif request_id == 30:
        # Manager Sign in request handling
        print("Received Manager Sign in request")
        print(data)
        handle_manager_signin(data)  # Should not return a response to the client

    elif request_id == 40:
        # Employee's Shifts Request handling
        print("Received Employee's Shifts Request")
        handle_employee_shifts_request(data)

    elif request_id == 50:
        # Manager Shifts inserting Request handling
        print("Received Manager Shifts inserting Request")
        handle_manager_shifts(data)

    elif request_id == 60:
        # Employees list request handling
        print("Received Employees list request")
        response = handle_employee_list()
        return response

    elif request_id == 70:
        # Employees list request handling
        print("Send user profile")
        profile_data = handle_send_profile()
        return {"request_id": request_id, "success": True, "data": profile_data}

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
            print("res:", response)

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for {websocket.remote_address}")


async def start_server():
    db, _ = initialize_database_and_session()
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Server started")
        await asyncio.Future()  # Keep the server running until Enter is pressed


asyncio.run(start_server())

if __name__ == "__main__":
    asyncio.run(start_server())

import websockets
import asyncio
import json

from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.main import initialize_database_and_session
from Backend.user_session import UserSession

# Initialize the database and session
db, _ = initialize_database_and_session()

# Global variable declaration
user_session = None


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
    user_controller = UsersController(db)
    user_controller.create_entity(data)


def handle_employee_shifts_request(data):
    pass


def handle_manager_shifts(data):
    pass


def handle_employee_list():
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_user_id()
        print(user_id)
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        print(workplace_id)
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


def handle_send_profile():
    pass


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
        handle_manager_signin(data)

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
        handle_send_profile()

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
    db, _ = initialize_database_and_session()
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Server started")
        await asyncio.Future()  # Keep the server running until Enter is pressed


asyncio.run(start_server())

if __name__ == "__main__":
    asyncio.run(start_server())

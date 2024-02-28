from __future__ import annotations
from Backend.main import initialize_database_and_session
import websockets
import asyncio
import json
from handlers import employee_list, employee_shifts_request, employee_signin, get_employee_requests, login, \
    manager_insert_shifts, manager_signin, send_profile

# Global variable declaration for the user session
user_session = None


def handle_request(request_id, data):
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

    Raises: ValueError if the user session is None and the request_id is not login or signin.

    Returns: The response from the handler to be sent back to the client.
    """
    global user_session  # Use the global user_session variable

    # If the user session is None and the request_id is not login or signin (10, 20, or 30) raise a ValueError
    if user_session is None and request_id not in {10, 20, 30}:
        raise ValueError("User session is None for request ID:", request_id)

    if request_id == 10:
        # Login request handling
        print("Received Login request")
        print(data)
        response, user_session = login.handle_login(data)
        return response

    elif request_id == 20:
        # Employee Sign in request handling
        print("Received Employee Sign in request")
        user_session = employee_signin.handle_employee_signin(data)

    elif request_id == 30:
        # Manager Sign in request handling
        print("Received Manager Sign in request")
        user_session = manager_signin.handle_manager_signin(data)

    elif request_id == 40:
        # Employee's Shifts Request handling
        print("Received Employee's Shifts Request")
        employee_shifts_request.handle_employee_shifts_request(data, user_session)

    elif request_id == 50:
        # Manager Get Employees Requests Request
        print("Received Manager Get Employees Requests Request")
        return get_employee_requests.handle_get_employee_requests(data, user_session)

    elif request_id == 55:
        # Manager Shifts inserting Request handling
        print("Received Manager Shifts inserting Request")
        manager_insert_shifts.handle_manager_insert_shifts(data, user_session)

    elif request_id == 60:
        # Employees list request handling
        print("Received Employees list request")
        return employee_list.handle_employee_list(user_session)

    elif request_id == 70:
        # Employees list request handling
        print("Send user profile")
        profile_data = send_profile.handle_send_profile(user_session)
        return {"request_id": request_id, "success": True, "data": profile_data}

    elif request_id == 80:
        # Make new week shifts
        print("Make new week shifts")
        manager_insert_shifts.make_shifts(user_session)

    else:
        print("Unknown request ID:", request_id)


async def handle_client(websocket):
    """
    Handle communication with a client over a WebSocket connection.

    Args:
        websocket: The WebSocket connection to the client.
    """
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
    """
    Start the WebSocket server and handle incoming connections.

    The server will listen on localhost:8080.
    Pressing Enter will stop the server.
    Note: The server uses the handle_client function to manage communication with clients.

    Raises:
        asyncio.CancelledError: Raised when the server is stopped.
        Exception: Raised for unexpected errors during server initialization.
    """
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


if __name__ == "__main__":
    asyncio.run(start_server())

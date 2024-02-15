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
    Handle the request based on the request_id and send the data to the appropriate handler (in Backend/handlers folder)
    Args:
        request_id: 2-digit number representing the request type (e.g. 10 for login request).
        data: The content of the request.

    Returns: The response from the handler to be sent back to the client.
    """
    global user_session  # Use the global user_session variable

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


if __name__ == "__main__":
    asyncio.run(start_server())

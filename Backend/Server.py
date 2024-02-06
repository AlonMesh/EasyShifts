import websockets
import asyncio
import json
from Backend.main import initialize_database_and_session

def handle_login(data):
    pass

def handle_employee_signin(data):
    pass

def handle_manager_signin(data):
    pass

def handle_employee_shifts_request(data):
    pass

def handle_manager_shifts(data):
    pass

def handle_employee_list(data):
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
        handle_login(data)

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
        # Manager Shifts inserting Request handling
        print("Received Manager Shifts inserting Request")
        handle_manager_shifts(data)

    elif request_id == 60:
        # Employees list request handling
        print("Received Employees list request")
        handle_employee_list(data)

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

            handle_request(request_id, request_data)

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for {websocket.remote_address}")

async def start_server():
    db, _  = initialize_database_and_session();
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Server started")
        await asyncio.Future()  # Keep the server running until Enter is pressed

asyncio.run(start_server())
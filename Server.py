import websockets

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

def get_request(data):
    # Assuming the request ID is the first two bytes of the received data
    request_id = int.from_bytes(data[:2], byteorder='big')
    # Extract the rest of the data
    request_data = data[2:].decode()
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

def handle_client(websocket):
    try:
        data = websocket.recv()
        print("Received:", data)

        # Get the request ID and data from the received packet
        request_id, request_data = get_request(data.encode())

        # Handle the request based on the request ID
        handle_request(request_id, request_data)

        # Example: Respond to the client
        response = "Request handled successfully!"
        websocket.send(response)

    finally:
        # Clean up the connection
        print("Connection closed")

def start_server():
    # Start the WebSocket server
    with websockets.serve(handle_client, "localhost", 8080):
        print("Server started")
        input("Press Enter to exit...")  # Keep the server running until Enter is pressed

if __name__ == "__main__":
    start_server()

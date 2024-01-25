import socket

def handle_login(data):
def handle_employee_signin(data):
def handle_manager_signin(data):
def handle_employee_shifts_request(data):
def handle_manager_shifts(data):
def handle_employee_list(data):

def get_request(data):
    # Assuming the request ID is the first two bytes of the received data
    request_id = int.from_bytes(data[:2], byteorder='big')
    # Extract the rest of the data
    request_data = data[2:].decode()
    return request_id, request_data

def handle_request (request_id, data):
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
def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('127.0.0.1', 8080)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)  # Maximum 5 connections in the queue

    print("Server is listening on {}:{}".format(*server_address))

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()

        try:
            print("Connection established with", client_address)
            handle_client(connection, client_address)

        finally:
            # Clean up the connection
            connection.close()


def handle_client(connection, address):
    try:
        print("Connection established with", address)

        while True:
            # Receive data from the client
            data = connection.recv(1024)
            if not data:
                # If no data is received, break the loop
                break

            print("Received:", data.decode())

            # Get the request ID and data from the received packet
            request_id, request_data = get_request(data)

            # Handle the request based on the request ID
            handle_request(request_id, request_data)

            # Example: Respond to the client
            response = "Request handled successfully!"
            connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()


if __name__ == "__main__":
    start_server()

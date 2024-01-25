import socket

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

            # Receive data from the client
            data = connection.recv(1024)
            print("Received:", data.decode())

            # Here you can process the received data and respond accordingly

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    start_server()

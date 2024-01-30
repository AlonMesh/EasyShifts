import asyncio
import websockets

async def handle_login(data):
    pass

async def handle_employee_signin(data):
    pass

async def handle_manager_signin(data):
    pass

async def handle_employee_shifts_request(data):
    pass

async def handle_manager_shifts(data):
    pass

async def handle_employee_list(data):
    pass

def get_request(data):
    # Assuming the request ID is the first two bytes of the received data
    request_id = int.from_bytes(data[:2], byteorder='big')
    # Extract the rest of the data
    request_data = data[2:].decode()
    return request_id, request_data

async def handle_request(request_id, data):
    if request_id == 10:
        # Login request handling
        print("Received Login request")
        await handle_login(data)

    elif request_id == 20:
        # Employee Sign in request handling
        print("Received Employee Sign in request")
        await handle_employee_signin(data)

    elif request_id == 30:
        # Manager Sign in request handling
        print("Received Manager Sign in request")
        await handle_manager_signin(data)

    elif request_id == 40:
        # Employee's Shifts Request handling
        print("Received Employee's Shifts Request")
        await handle_employee_shifts_request(data)

    elif request_id == 50:
        # Manager Shifts inserting Request handling
        print("Received Manager Shifts inserting Request")
        await handle_manager_shifts(data)

    elif request_id == 60:
        # Employees list request handling
        print("Received Employees list request")
        await handle_employee_list(data)

    else:
        print("Unknown request ID:", request_id)

async def handle_client(websocket, path):
    try:
        async for data in websocket:
            print("Received:", data)

            # Get the request ID and data from the received packet
            request_id, request_data = get_request(data.encode())

            # Handle the request based on the request ID
            await handle_request(request_id, request_data)

            # Example: Respond to the client
            response = "Request handled successfully!"
            await websocket.send(response)

    finally:
        # Clean up the connection
        print("Connection closed")

async def start_server():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Server started")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())

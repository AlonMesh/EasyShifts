from __future__ import annotations
from Backend.handlers.employee_list import handle_employee_approval, handle_employee_rejection
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client
from Backend.user_session import UserSession
from Backend.main import initialize_database_and_session
import websockets
import asyncio
import json
from Backend.handlers import login, employee_signin, manager_signin, employee_shifts_request, \
    get_employee_requests, manager_insert_shifts, employee_list, send_profile, manager_schedule, \
    send_shifts_to_employee, make_shifts
# Initialize the database and session
db, _ = initialize_database_and_session()

# Global variable declaration
user_session: UserSession | None = None


def handle_request(request_id, data):
    global user_session
    if request_id == 10:
        # Login request handling
        print("Received Login request")
        print(data)

        response, user_session = login.handle_login(data)
        return {"request_id": request_id, "data": response}

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
        return {"request_id": request_id, "success": True}

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

    elif request_id == 62:
        # Employee approval request handling
        print("Received Employee Approval request")
        return {"success": handle_employee_approval(data, user_session)}

    elif request_id == 64:
        # Employee rejection request handling
        print("Received Employee Rejection request")
        return {"success": handle_employee_rejection(data, user_session)}

    elif request_id == 70:
        # Send user profile handling
        print("Send user profile")
        profile_data = send_profile.handle_send_profile(user_session)
        return {"request_id": request_id, "success": True, "data": profile_data}

    elif request_id == 80:
        # Make new week shifts
        print("Make new week shifts")
        make_shifts.make_shifts(user_session)

    elif request_id == 90:
        # Get Employee's shifts handling
        print("Send employees shifts")
        employees_shifts = send_shifts_to_employee.handle_send_shifts(user_session)
        return employees_shifts

    elif request_id == 91:
        # Get Employees Requests Data
        print("Get Employees Requests Data")
        res = manager_schedule.watch_workers_requests(user_session)
        print(res)
        return {"request_id": request_id, "data": res}

    elif request_id == 93:
        # Get all workers
        print("Get all workers")
        res = manager_schedule.get_all_workers_names_by_workplace_id(user_session)
        print(res)
        return {"request_id": request_id, "data": res}

    elif request_id == 95:
        # Get preferences
        print("Get preferences")
        res = manager_schedule.handle_get_preferences(user_session)
        print(res)
        return {"request_id": request_id, "data": res}

    elif request_id == 97:
        # Get start date
        print("Get start date")
        res = manager_schedule.handle_get_start_date(user_session).isoformat()  # Convert to ISO format
        print(res)
        return {"request_id": request_id, "data": res}

    elif request_id == 98:
        # Get assigned shifts
        print("Get assigned shifts")
        res = manager_schedule.handle_get_assigned_shifts(user_session, data)
        print(res)
        return {"request_id": request_id, "data": res}

    elif request_id == 99:
        # Change schedule
        print("Get change schedule")
        manager_schedule.handle_schedules(user_session.get_id, data)
        return {"request_id": request_id, "success": True}

    elif request_id == 991:
        # Set preferences
        print("Set preferences")
        manager_schedule.handle_save_preferences(user_session.get_id, data)
        return {"request_id": request_id, "success": True}

    elif request_id == 992:
        # Set schedule window time
        print("Set schedule window time")
        manager_schedule.open_requests_windows(user_session.get_id, data)
        manager_schedule.get_last_shift_board_window_times(user_session.get_id)
        return {"request_id": request_id, "success": True}

    else:
        print("Unknown request ID:", request_id)


async def handle_client(websocket, path):
    print("new client connected")
    try:
        async for message in websocket:
            # Parse the JSON message
            data = json.loads(message)
            print("Received data:", data)

            # Extract the request_id and data
            request_id = data.get('request_id', None)
            request_data = data.get('data', None)

            print("Request ID:", request_id)
            print("Data:", request_data)

            response = handle_request(request_id, request_data)
            json_data = json.dumps(response)
            await websocket.send(json_data)
            print(response)
    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for {websocket.remote_address}")
    except Exception as e:
        if "User session not found" in str(e):
            # Handle the "User session not found" exception here
            print("User session not found. Sending an appropriate response.")
            await websocket.send("User session not found. Please log in.")
        else:
            # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            await websocket.send("An unexpected error occurred. Please try again later.")


async def start_server():
    try:
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

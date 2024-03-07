from datetime import timedelta, datetime
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController
from Backend.db.models import ShiftBoard
from Backend.user_session import UserSession
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client
from Backend.config.constants import db, next_sunday


def handle_create_new_board(user_session: UserSession):
    # Create a controller for the shift board
    shift_board_controller = ShiftBoardController(db)

    # In case the manager wants to create his first board
    try:
        shift_board_controller.get_last_shift_board(user_session.get_id)
    except IndexError:
        # Create a new shift board
        board = shift_board_controller.create_shift_board(
            {"weekStartDate": next_sunday, "workplaceID": user_session.get_id})
        return board

    # Get the last shift board
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Create a new shift board
    new_week_start_date = last_board.weekStartDate + timedelta(days=7)  # A week after the last shift board
    new_board = shift_board_controller.create_shift_board(
        {"weekStartDate": new_week_start_date, "workplaceID": user_session.get_id})

    # Return the new shift board
    return new_board


def handle_get_board(user_session: UserSession) -> dict:
    # Get the last shift board
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Extract the content from the shift board
    content = last_board.content

    # Return the shift board as a dictionary (JSON)
    return content


def handle_get_start_date(user_session: UserSession) -> dict:
    # Get the last shift board
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Extract the start date from the shift board
    start_date = last_board.weekStartDate

    # Return the start date as a dictionary (JSON)
    return start_date


def handle_save_board(data, user_session: UserSession) -> ShiftBoard:
    # Get the week_start_date from the data
    week_start_date = data["week_start_date"]  # TODO: Depending on the client!

    # Extract the content from the data
    content = data["content"]  # TODO: Depending on the client!

    # Update the shift board
    shift_board_controller = ShiftBoardController(db)
    updated_shift_board = shift_board_controller.update_shift_board(week_start_date, user_session.get_id, content)

    # Return the updated shift board
    return updated_shift_board


def handle_reset_board(user_session: UserSession) -> ShiftBoard:
    # Get the last shift board (Assuming it is the last shift board, the others are published)
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Update the shift board with the default content
    updated_board = shift_board_controller.update_shift_board(last_board.weekStartDate, user_session.get_id,
                                                              {"content": {}})

    # Return the updated shift board
    return updated_board


def handle_publish_board(user_session: UserSession) -> bool:
    # Publish the shift board (Assuming it is the last shift board, the others are published)
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.publish_shift_board(next_sunday, user_session.get_id)

    # Return True if the shift board is published
    return shift_board_controller.get_last_shift_board(user_session.get_id).is_published


def handle_unpublish_board(user_session: UserSession) -> bool:
    # Unpublish the shift board (Assuming it is the last shift board, the others are published)
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.unpublish_shift_board(next_sunday, user_session.get_id)

    # Return True if the shift board is unpublished
    return not shift_board_controller.get_last_shift_board(user_session.get_id).is_published


def handle_get_board_content(user_session: UserSession) -> dict:
    # Get the last shift board (Assuming it is the last shift board, the others are published)
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Return the content of the shift board
    return last_board.content


def schedule_worker_to_shift(shift_id, worker_id) -> bool:
    # Assume the data is a dictionary containing the worker's ID and the shift's ID
    shift_workers_data = {
        "shiftID": shift_id,
        "userID": worker_id
    }

    # Schedule the worker to the shift
    shift_workers_controller = ShiftWorkersController(db)
    shift_workers_controller.create_entity(shift_workers_data)

    # Return True if the worker is scheduled to the shift
    return True


def unschedule_worker_from_shift(shift_id, worker_id) -> bool:
    # Unschedule the worker from the shift
    shift_workers_controller = ShiftWorkersController(db)
    shift_workers_controller.delete_entity_shift_worker(shift_id, worker_id)

    # Return True if the worker is unscheduled from the shift
    return True


def handle_schedules(workplace_id, data: dict) -> bool:
    print("workplace_id: ", workplace_id)
    print("data: ", data)
    # Been called from the client every time a worker is scheduled or unscheduled from a shift

    # The data is a dictionary of worker's name and shift's day and part
    worker_name = data["worker_name"]["name"]
    shift_day = data["day"]
    shift_part = data["part"]

    print("worker_name: ", worker_name)
    print("shift_day: ", shift_day)
    print("shift_part: ", shift_part)

    # Get the worker's ID
    workplace_controller = WorkPlacesController(db)
    worker = workplace_controller.get_worker_by_name(workplace_id, worker_name)

    # Create shift_date based on next_sunday and shift_day (sunday, monday, etc.)
    shift_date = next_sunday + timedelta(days=convert_day_name_to_number(shift_day))

    # Get the shift's ID
    shift_controller = ShiftsController(db)
    shift = shift_controller.get_shift_by_day_and_part(workplace_id, shift_date, shift_part)

    if shift is None:
        # If the shift does not exist, create it
        shift = shift_controller.create_entity(
            {"workPlaceID": workplace_id, "shiftDate": shift_date, "shiftPart": shift_part})

    print("To schedule worker to shift:", shift.id, worker.id, data["type"])

    if data["type"] == "addShift":
        # Schedule the worker to the shift
        return schedule_worker_to_shift(shift.id, worker.id)

    elif data["type"] == "removeShift":
        # Unschedule the worker from the shift
        return unschedule_worker_from_shift(shift.id, worker.id)

    else:
        raise ValueError("Unknown type")


def convert_day_name_to_number(day_name: str) -> int:
    # Convert the day name to a number
    day_name_to_number = {
        "sunday": 0,
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6
    }
    return day_name_to_number[day_name]


def watch_workers_requests(user_session: UserSession):
    # Get a list of all workers in the workplace
    workplace_controller = WorkPlacesController(db)
    workers = workplace_controller.get_all_workers_by_workplace_id(user_session.get_id)

    # Get only workers where worker.isApproval is True
    workers = [worker for worker in workers if worker.isApproval]

    # Extract the IDs and names of the workers
    workers_info = [(worker.id, worker.name) for worker in workers]

    # Get all requests from the workers
    user_requests_controller = UserRequestsController(db)

    # Get the start and end datetimes for the requests window
    shift_board_controller = ShiftBoardController(db)
    relevant_shift_board = shift_board_controller.get_last_shift_board(user_session.get_id)
    requests_window_start = relevant_shift_board.requests_window_start
    requests_window_end = relevant_shift_board.requests_window_end

    combined_list = [None] * len(workers_info)
    user_controller = UsersController(db)

    for i, (worker_id, name) in enumerate(workers_info):
            combined_list[i] = {"name": name,
                                "request_content": user_requests_controller.get_request_by_userid(worker_id)}

    # Return the combined list
    return combined_list


def open_requests_windows(workplace_id, data: dict) -> bool:
    # Extract the start and end datetimes for the requests window
    requests_window_start = data["requests_window_start"]
    requests_window_end = data["requests_window_end"]

    # Convert the datetimes to datetime objects
    requests_window_start = datetime.strptime(requests_window_start, "%Y-%m-%dT%H:%M:%S.%fZ")
    requests_window_end = datetime.strptime(requests_window_end, "%Y-%m-%dT%H:%M:%S.%fZ")

    updated_data = {"requests_window_start": requests_window_start, "requests_window_end": requests_window_end}

    # Update the shift board with the new requests window
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.update_shift_board(next_sunday, workplace_id, updated_data)

    # Return True if the requests window is open
    return True


def get_last_shift_board_window_times(workplace_id):
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(workplace_id)
    print("Open requests window times: ", last_board.requests_window_start, last_board.requests_window_end)
    return last_board.requests_window_start, last_board.requests_window_end


def handle_get_preferences(user_session: UserSession) -> dict:
    # Get the last shift board
    shift_board_controller = ShiftBoardController(db)
    last_board = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Extract the preferences from the shift board
    preferences = last_board.preferences

    # Return the preferences as a dictionary (JSON)
    return preferences


def handle_save_preferences(workplace_id, data: dict) -> bool:
    # Extract the preferences from the data
    number_of_shifts_per_day = data["number_of_shifts_per_day"]
    closed_days = data["closed_days"]

    # Create a dictionary with the preferences
    new_preferences = {
        "number_of_shifts_per_day": number_of_shifts_per_day,
        "closed_days": closed_days
    }

    print("new_preferences: ", new_preferences)

    # Update the shift board with the new preferences
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.update_shift_board(next_sunday, workplace_id, {"preferences": new_preferences})

    # Return True if the preferences are saved
    return True


def get_all_workers_names_by_workplace_id(user_session):
    # Get all workers in the workplace
    workplace_controller = WorkPlacesController(db)
    workers = workplace_controller.get_all_workers_by_workplace_id(user_session.get_id)

    # Get only workers where worker.isApproval is True
    workers = [worker for worker in workers if worker.isApproval]

    # Extract the names of the workers
    workers_names = [worker.name for worker in workers]

    # Return the names of the workers
    return workers_names


def handle_get_assigned_shifts(user_session, data):
    print("data: ", data)
    # data represents start and end dates
    start_date_str = data["start_date"]

    print("start_date_str: ", start_date_str)

    # Convert the start date to a datetime object
    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Get the end date, a week after the start date
    end_date = start_date + timedelta(days=7)

    # Create an array where each element is a dictionary with the worker's name and the shifts he is assigned to
    assigned_shifts = []

    # Get all workers in the workplace
    workplace_controller = WorkPlacesController(db)
    workers = workplace_controller.get_all_workers_by_workplace_id(user_session.get_id)

    # Iterate over the workers
    for worker in workers:
        # Get all shifts assigned to the worker
        shifts_controller = ShiftsController(db)
        shifts = shifts_controller.get_all_shifts_between_dates_for_given_worker(worker.id, start_date, end_date)

        # Convert the shifts to a format that the client can understand
        converted_shifts = convert_shifts_for_client(shifts, db)

        # Add the worker's name and the shifts he is assigned to the array
        assigned_shifts.append({"name": worker.name, "shifts": converted_shifts})

    # Return the array
    print("assigned_shifts: ", assigned_shifts)
    return assigned_shifts

from datetime import timedelta
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController
from Backend.db.models import ShiftBoard
from Backend.user_session import UserSession
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.db.controllers.userRequests_controller import UserRequestsController
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
    board_data = shift_board_controller.get_last_shift_board(user_session.get_id)

    # Return the shift board as a dictionary (JSON)
    return board_data


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


def schedule_worker_to_shift(data: dict) -> bool:
    # Assume the data is a dictionary containing the worker's ID and the shift's ID
    shift_workers_data = {
        "shift_id": data["shift_id"],  # TODO: Depending on the client!
        "worker_id": data["worker_id"]  # TODO: Depending on the client!
    }

    # TODO: try to schedule the worker to the shift
    # Schedule the worker to the shift
    shift_workers_controller = ShiftWorkersController(db)
    shift_workers_controller.create_entity(shift_workers_data)

    # Return True if the worker is scheduled to the shift
    return True


def unschedule_worker_from_shift(data: dict) -> bool:
    # Delete the shiftworkers entity
    shift_workers_controller = ShiftWorkersController(db)
    shift_workers_controller.delete_entity_shift_worker(data["shift_id"],
                                                        data["worker_id"])  # TODO: Depending on the client!

    # Return True if the worker is unscheduled from the shift
    return True


def handle_schedules(data: dict):
    # Get all schedules from the client and schedule/unschedule workers to shifts by calling the appropriate function
    pass


def watch_workers_requests(user_session: UserSession):
    # Get a list of all workers in the workplace
    workplace_controller = WorkPlacesController(db)
    workers = workplace_controller.get_all_workers_by_workplace_id(user_session.get_id)

    # Extract the IDs and names of the workers
    workers_info = [(worker.id, worker.name) for worker in workers]

    # Get all requests from the workers
    user_requests_controller = UserRequestsController(db)

    # Get the start and end datetimes for the requests window
    shift_board_controller = ShiftBoardController(db)
    relevant_shift_board = shift_board_controller.get_last_shift_board(user_session.get_id)
    requests_window_start = relevant_shift_board.requests_window_start
    requests_window_end = relevant_shift_board.requests_window_end

    # Create a dictionary with keys "name" and "request_content"
    combined_list = [
        {"name": name,
         "request_content": user_requests_controller.get_request_content_by_user_id_between_datetimes(worker_id,
                                                                                                      requests_window_start,
                                                                                                      requests_window_end)}
        # Iterate over workers_info to generate dictionaries for each worker
        for worker_id, name in workers_info
    ]

    # Return the combined list
    return combined_list


def open_requests_windows(data: dict, user_session: UserSession) -> bool:
    # Extract the start and end datetimes for the requests window
    requests_window_start = data["requests_window_start"]  # TODO: Depending on the client!
    requests_window_end = data["requests_window_end"]  # TODO: Depending on the client!
    updated_data = {"requests_window_start": requests_window_start, "requests_window_end": requests_window_end}

    # Update the shift board with the new requests window
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.update_shift_board(next_sunday, user_session.get_id, updated_data)

    # Return True if the requests window is open
    return True

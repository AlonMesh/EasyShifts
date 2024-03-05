from datetime import datetime
from Backend.config.constants import db
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.user_session import UserSession


def handle_employee_shifts_request(data, user_session):
    user_id = user_session.get_id
    shifts_string = data['shiftsString']

    shifts_request_data = {"id": user_id, "modifyAt": datetime.now(), "requests": shifts_string}
    user_request_controller = UserRequestsController(db)
    user_request_controller.update_entity(user_id, shifts_request_data)


def handle_is_in_request_window(user_session: UserSession) -> bool:  # When the user opens the user request page
    """
    Checks if the current date is within the request window for the user.

    Args:
        user_session (UserSession): The user session containing user information.

    Returns:
        bool: True if the current date is within the request window, False otherwise.
    """
    # Create a controller for the shift board
    shift_board_controller = ShiftBoardController(db)

    # Get manager id by worker id
    workPlaces_controller = WorkPlacesController(db)
    workplace_id = workPlaces_controller.get_workplace_id_by_user_id(user_session.get_id)

    print("workplace_id: ", workplace_id)

    # Get the last shift board
    last_shift_board = shift_board_controller.get_last_shift_board(workplace_id)

    # Check if the current date is in the request window
    if last_shift_board.requests_window_start <= datetime.now() <= last_shift_board.requests_window_end:
        return True

    return False

from Backend.db.models import ShiftBoard
from Backend.user_session import UserSession
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.config.constants import db, next_sunday


def handle_create_new_board():
    pass


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
    updated_board = shift_board_controller.update_shift_board(last_board.week_start_date, user_session.get_id,
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


def schedule_worker_to_shift():
    # Creating a shiftworkers entity based on a dict data
    pass


def unschedule_worker_from_shift():
    # Delete the shiftworkers entity
    pass


def watch_workers_requests():
    pass

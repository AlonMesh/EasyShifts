from Backend.config.constants import db
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client


def handle_send_shifts(user_session):
    if user_session is None:
        raise Exception("User session not found.")

    user_id = user_session.get_id
    shifts_controller = ShiftsController(db)
    future_shifts = shifts_controller.get_future_shifts_for_user(user_id)
    future_shifts_for_client = convert_shifts_for_client(future_shifts, db, is_manager=False)
    return future_shifts_for_client

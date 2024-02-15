from datetime import datetime
from Backend.config.constants import db
from Backend.db.controllers.userRequests_controller import UserRequestsController


def handle_employee_shifts_request(data, user_session):
    if user_session is None:
        print("User session not found.")
        return False
    user_id = user_session.get_id
    shifts_string = data.get('shiftsString')

    shifts_request_data = {"id": user_id, "modifyAt": datetime.now(), "requests": shifts_string}
    user_request_controller = UserRequestsController(db)
    user_request_controller.update_entity(user_id, shifts_request_data)

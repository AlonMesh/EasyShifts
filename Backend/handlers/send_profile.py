from Backend.config.constants import db
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shifts_for_client
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.user_session import UserSession


def handle_send_profile(user_session: UserSession) -> dict:
    """
    Handles the request to send the user's profile data to the client.

    Returns:
        dict: A dictionary containing the user's profile data.
              The structure of the dictionary depends on the user's role (manager or worker).
    Raises:
        Exception: If the user session is not found.
    """
    if user_session is None:
        raise Exception("User session not found.")

    # Retrieve the user ID from the user session
    user_id = user_session.get_id

    # Initialize the users controller
    users_controller = UsersController(db)

    # Initialize the workplaces controller
    work_places_controller = WorkPlacesController(db)

    # Initialize the shifts controller
    shifts_controller = ShiftsController(db)

    # Create a dictionary to hold the returned data by key-value pairs
    returned_data = {
        "user_id": user_id,
        "username": users_controller.get_username_by_id(user_id)
    }

    # Retrieve the user's profile
    if user_session.can_access_manager_page():
        # Add manager-specific data to the dictionary
        returned_data["workplace_name"] = users_controller.get_name_by_id(user_id)  # name of manager = workplace name
        future_shifts = shifts_controller.get_future_shifts_for_workplace(user_id)  # user_id of manager = workplace_id
        future_shifts_for_client = convert_shifts_for_client(future_shifts, db)
        returned_data["future_shifts"] = future_shifts_for_client
    else:
        # Add worker-specific data to the dictionary
        returned_data["name"] = users_controller.get_name_by_id(user_id)
        returned_data["workplace_name"] = work_places_controller.get_workplace_name_by_worker_id(user_id)
        future_shifts = shifts_controller.get_future_shifts_for_user(user_id)
        future_shifts_for_client = convert_shifts_for_client(future_shifts, db, is_manager=False)
        returned_data["future_shifts"] = future_shifts_for_client

    # Return the dictionary
    return returned_data

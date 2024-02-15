from Backend.config.constants import db
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.user_session import UserSession


def handle_employee_list(user_session: UserSession) -> str:
    # TODO: No workers -> crushed. Should return "No workers found"
    # TODO: This returns bools, fix it
    # TODO: This is a manager-specific page, so the user_session should be a manager
    # TODO: I offer to change the return type to List[dict[str, str]] which stands for id and name of the worker
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_id
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        if workplace_id is not None:
            # Assuming get_active_workers_for_user returns a list of active workers
            active_workers = work_places_controller.get_active_workers_for_user(user_id)

            # Convert list of tuples to a string
            active_workers_str = ' ,'.join(f'{worker[0]}: {worker[1]}' for worker in active_workers)

            return active_workers_str  # return active workers as a string
        else:
            print("User does not work in any workplace.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False

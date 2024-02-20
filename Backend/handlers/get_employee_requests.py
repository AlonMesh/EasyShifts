from Backend.config.constants import db
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController


def handle_get_employee_requests(data, user_session):
    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        user_id = user_session.get_id
        workplace_id = work_places_controller.get_workplace_id_by_user_id(user_id)
        if workplace_id is not None:
            # Assuming get_active_workers_for_user returns a list of active workers
            active_workers = work_places_controller.get_active_workers_for_user(user_id)
            employees_requests = {}
            user_requests_controller = UserRequestsController(db)
            for worker in active_workers:
                employees_requests[worker[1]] = user_requests_controller.get_request_by_userid(worker[0])

            return employees_requests

        else:
            print("User does not work in any workplace.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False

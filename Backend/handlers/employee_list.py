from Backend.config.constants import db
from Backend.db.controllers import users_controller
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.user_session import UserSession
import json


def handle_employee_list(user_session: UserSession) -> str:
    if user_session is None:
        print("User session not found.")
        return json.dumps({"success": False, "error": "User session not found."})

    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        manager_id = user_session.get_id
        workplace_id = work_places_controller.get_workplace_id_by_user_id(manager_id)
        if workplace_id is not None:
            # Assuming get_active_workers_for_user returns a list of active workers
            active_workers_approved = work_places_controller.get_active_approve_workers_for_user(manager_id)
            active_workers_unapproved = work_places_controller.get_active_unapprove_workers_for_user(manager_id)

            # Convert list of tuples to a list of dictionaries
            active_workers = []
            for worker in active_workers_approved:
                active_workers.append({"userName": worker[0], "name": worker[1], "approved": True})
            for worker in active_workers_unapproved:
                active_workers.append({"userName": worker[0], "name": worker[1], "approved": False})

            # Return the list of employees as a dictionary
            return active_workers
        else:
            print("User does not work in any workplace.")
            return json.dumps({"success": False, "error": "User does not work in any workplace."})
    else:
        print("User does not have access to manager-specific pages.")
        return json.dumps({"success": False, "error": "User does not have access to manager-specific pages."})


def handle_employee_approval(data, user_session):
    """
    Handles the approval of an employee.

    Parameters:
        data (dict): A dictionary containing the employee ID.
        users_controller (UsersController): An instance of UsersController for user management.

    Returns:
        bool: True if the approval was successful, False otherwise.
    """
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        user_name = data.get('userName')
        if user_name:
            # Create an instance of UsersController
            users_controller_instance = UsersController(db)
            # Call approve_user method on the instance
            users_controller_instance.approve_user(user_name)
            return True
        else:
            print("Employee userName not provided in the data.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False


def handle_employee_rejection(data, user_session):
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        # Access the UsersController
        users_controller = UsersController(db)
        workPlacees_controller = WorkPlacesController(db)
        # Extract the employee userName from the data
        user_name = data.get('userName')

        # Get the user ID using the username
        user_id = users_controller.get_user_id_by_username(user_name)

        if user_id is not None:
            workPlacees_controller.delete_entity(user_id)

            deleted_entity = users_controller.delete_entity(user_id)

            if deleted_entity:
                print(f"Employee with userName {user_name} has been successfully deleted.")
                return True
            else:
                print(f"Failed to delete employee with userName {user_name}.")
                return False
        else:
            print(f"No user found with userName {user_name}.")
            return False
    else:
        print("User does not have access to manager-specific pages.")
        return False

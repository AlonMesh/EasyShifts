from Backend.config.constants import db
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.db.controllers.users_controller import UsersController
from Backend.handlers.login import handle_login
from Backend.config.constants import next_sunday
from Backend.handlers.auth.authentication import BackendAuthenticationUser


def handle_manager_signin(data):  # TODO: modify the function as the data will be different, including preferences!!!
    """
        Handles the manager signin process by creating a new user using the UsersController.

        Parameters:
            data (dict): A dictionary containing user data for signin.
                Example: {'username': 'manager1', 'password': '123', 'isManager': True,
                 'isActive': True, 'isApproval': True, 'name': 'Place Name'}
        """

    # Initialize the users controller, passing the database session
    user_controller = UsersController(db)
    user_controller.create_entity(data)

    # Send the username and password to the login function to create a user session
    login_data = {"username": data["username"], "password": data["password"]}

    # Send the username and password to the login function to create a user session
    _, user_session = handle_login(login_data)  # Depends on the `handle_login` function to work properly.

    # Create a ShiftBoard for the new manager
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.create_shift_board({
        "weekStartDate": next_sunday,
        "workplaceID": user_session.get_id,
        "isPublished": False,
        "content": "",
    })

    return user_session

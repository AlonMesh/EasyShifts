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
    # Validate the user registration
    auth = BackendAuthenticationUser(data['register_details']['username'], data['register_details']['password'])
    if not auth.validate_registration():
        # TODO: raise error to the client
        pass

    # Extract details and preferences from the data
    register_details = data['register_details']
    preferences = data['preferences']

    # Initialize the users controller, passing the database session
    user_controller = UsersController(db)
    user_controller.create_entity(register_details)

    # Send the username and password to the login function to create a user session
    login_data = {"username": register_details["username"], "password": register_details["password"]}

    # Send the username and password to the login function to create a user session
    _, user_session = handle_login(login_data)  # Depends on the `handle_login` function to work properly.

    # Create a ShiftBoard for the new manager
    shift_board_controller = ShiftBoardController(db)
    shift_board_controller.create_shift_board({
        "weekStartDate": next_sunday,
        "workplaceID": user_session.get_id,
        "isPublished": False,
        "content": "",
        "preferences": preferences
    })

    return user_session

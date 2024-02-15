from Backend.config.constants import db
from Backend.db.controllers.users_controller import UsersController
from Backend.handlers.login import handle_login


def handle_manager_signin(data):
    """
        Handles the manager signin process by creating a new user using the UsersController.

        Parameters:
            data (dict): A dictionary containing user data for signin.
                Example: {'username': 'manager1', 'password': '123', 'isManager': True,
                 'isActive': True, 'isApproval': True, 'name': 'Place Name'}
        """
    # TODO: Add a check to see if the user is already logged in. If so, return an error message to the client.

    # TODO: Add a check to see if the username already exists. If so, return an error message to the client.

    # TODO: Add a check to see if the workplace name already exists. If so, return an error message to the client.

    # TODO: Add a check to see if username is valid. If not, return an error message to the client.

    # TODO: Add a check to see if password is valid. If not, return an error message to the client.

    # Initialize the users controller, passing the database session
    user_controller = UsersController(db)
    user_controller.create_entity(data)

    # Send the username and password to the login function to create a user session
    login_data = {"username": data["username"], "password": data["password"]}

    # Send the username and password to the login function to create a user session
    _, user_session = handle_login(login_data)  # Depends on the `handle_login` function to work properly.
    return user_session

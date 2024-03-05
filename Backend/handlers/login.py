from Backend.db.controllers.users_controller import UsersController
from Backend.user_session import UserSession
from Backend.main import initialize_database_and_session

# Initialize the database and session
db, _ = initialize_database_and_session()


def handle_login(data):
    # Access the username and password
    username = data['username']
    password = data['password']

    # Initialize the users controller, passing the database session
    users_controller = UsersController(db)

    # Check if the user exists and is a manager
    user_exists, is_manager = users_controller.check_user_existence_and_manager_status(username, password)

    try:
        # Retrieve the actual user ID from the database
        user_id = users_controller.get_user_id_by_username_and_password(username, password)

        # Create a UserSession object if the user exists
        user_session = UserSession(user_id=user_id, is_manager=is_manager)
    except ValueError:
        raise ValueError("User does not exist")

    # Return if the user exists and is a manager, and the user session
    response = {
        "user_exists": user_exists,
        "is_manager": is_manager
    }
    return response, user_session

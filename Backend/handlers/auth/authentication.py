from sqlalchemy.exc import NoResultFound
from Backend.config.constants import db
from Backend.db.controllers.users_controller import UsersController


class BackendAuthenticationUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.users_controller = UsersController(db)
        self.error_message = ""

    def __is_user_exists(self):
        """
        Checks if the user exists in the database.

        Returns: True if the user exists, else False.
        """
        try:
            self.users_controller.get_entity(self.username)
            return True
        except NoResultFound:
            self.error_message = f"User with username {self.username} does not exist"
            return False

    def __is_username_and_password_match(self):
        """
        Checks if the username and password match.

        Returns: True if the username and password match, else False.
        """
        user = self.users_controller.get_entity(self.username)
        if user.password == self.password:
            return True
        else:
            self.error_message = "Username and password do not match"
            return False

    def validate_login(self):
        """
        Validates the user login.

        Returns: True if the user is logged in, else False.
        """
        if self.__is_user_exists() and self.__is_username_and_password_match():
            return True
        else:
            return False

    def validate_registration(self):
        """
        Validates the user registration.

        Returns: True if the user is registered, else False.
        """
        if self.__is_user_exists():
            self.error_message = f"User with username {self.username} already exists"  # Overwrite the error message
            return False
        else:
            self.users_controller.create_entity({"username": self.username, "password": self.password})
            return True

    def get_error_message(self):
        """
        Returns: The error message that occurred during the login process.
        """
        return self.error_message

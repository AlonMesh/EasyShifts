from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.users_repository import UsersRepository
from Backend.db.services.users_service import UsersService
from typing import Tuple


class UsersController(BaseController):
    """
    UserController Class

    Controller class for managing user entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the UserController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        self.repository = UsersRepository(db)
        self.service = UsersService(self.repository)
        super().__init__(self.repository, self.service)

    def check_user_existence_and_manager_status(self, username: str, password: str) -> Tuple[bool, bool]:
        """
        Check if a user with the given username and password exists and if they are a manager.

        Parameters:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            Tuple[bool, bool]: A tuple of booleans. The first boolean indicates whether the user exists,
                               and the second boolean indicates whether the user is a manager.
        """
        # Delegate the functionality to the service layer
        return self.service.check_user_existence_and_manager_status(username, password)

    def get_user_id_by_username_and_password(self, username: str, password: str):
        """
        Retrieves the user ID by username and password.

        Parameters:
            username (str): The username of the user to retrieve.
            password (str): The password of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        return self.service.get_user_id_by_username_and_password(username, password)

    def get_user_id_by_username(self, username: str):
        """
        Retrieves the user ID by username.

        Parameters:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        return self.service.get_user_id_by_username(username)

    def get_user_id_by_name(self, name: str):
        """
        Retrieves the user ID by username.

        Parameters:
            name (str): The name of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        return self.service.get_user_id_by_name(name)

    def get_username_by_id(self, user_id: str):
        """
        Retrieves the username by user ID.

        Parameters:
            user_id (str): The user ID of the user to retrieve.

        Returns:
            Optional[str]: The username if the user exists, None otherwise.
        """
        return self.service.get_username_by_id(user_id)

    def get_name_by_id(self, user_id: str):
        """
        Retrieves the name by user ID.

        Parameters:
            user_id (int): The user ID of the user to retrieve.

        Returns:
            str: The name if the user exists, None otherwise.
        """
        return self.service.get_name_by_id(user_id)

    def approve_user(self, user_name: str):
        """
        Approve a user by setting isApproval to True.

        Parameters:
            user_name (str): The user_name of the user to approve.
        """
        # Call the repository method to approve the user
        self.repository.approve_user(user_name)

    def check_username_existence(self, username: str) -> bool:
        """
        Check if a username already exists in the database.

        Parameters:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        return self.repository.get_user_by_username(username) is not None

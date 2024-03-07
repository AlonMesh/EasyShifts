from Backend.db.repositories.users_repository import UsersRepository
from Backend.db.services.base_service import BaseService
from typing import Tuple


class UsersService(BaseService):
    """
    Service class for handling complexes operations.
    """

    def __init__(self, repository: UsersRepository):
        """
        Initializes the UsersService with a user repository.

        Parameters:
            repository: An instance of UsersRepository.
        """
        super().__init__(repository)

    def custom_operation(self):
        """
        Placeholder for a custom operation.
        Actual implementation is not provided yet.
        """
        pass

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
        # Check if the user exists
        user_exists = self.repository.check_user_credentials(username, password)

        # Check if the user is a manager
        is_manager = self.repository.is_manager_by_username_and_password(username, password)

        return user_exists, is_manager

    def get_user_id_by_username_and_password(self, username: str, password: str):
        """
        Retrieves the user ID by username and password.

        Parameters:
            username (str): The username of the user to retrieve.
            password (str): The password of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        user = self.repository.get_user_by_username_and_password(username, password)
        if user:
            return user.id
        return None

    def get_user_id_by_username(self, username: str):
        """
        Retrieves the user ID by username.

        Parameters:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        user = self.repository.get_user_by_username(username)
        if user:
            return user.id
        return None

    def get_user_id_by_name(self, name: str):
        """
        Retrieves the user ID by username.

        Parameters:
            name (str): The name of the user to retrieve.

        Returns:
            Optional[int]: The user ID if the user exists, None otherwise.
        """
        user = self.repository.get_user_by_name(name)
        if user:
            return user.id
        return None

    def get_username_by_id(self, user_id: str):
        """
        Retrieves the username by user ID.

        Args:
            user_id (int): The user ID of the user to retrieve.

        Raises:
            NoResultFound: If the user does not exist.

        Returns: The username if the user exists.

        """
        user = self.repository.get_entity(user_id)  # Raises an exception if the user does not exist
        return user.username

    def get_name_by_id(self, user_id: str):
        """
        Retrieves the name by user ID.

        Parameters:
            user_id (int): The user ID of the user to retrieve.

        Returns:
            str: The name if the user exists, None otherwise.
        """
        user = self.repository.get_entity(user_id)  # Raises an exception if the user does not exist
        return user.name






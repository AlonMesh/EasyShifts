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

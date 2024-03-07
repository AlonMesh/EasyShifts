from sqlalchemy.orm import Session
from Backend.db.models import User
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.repositories.userRequests_repository import UserRequestsRepository


class UsersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def delete_entity(self, entity_id: str):
        """
        """
        # If the user have a request, delete it
        userRequestsRepository = UserRequestsRepository(self.db)
        try:
            user_request = userRequestsRepository.get_entity(entity_id)
            if user_request:
                userRequestsRepository.delete_entity(entity_id)
        except:
            pass

        # Delete the user
        super().delete_entity(entity_id)

    def check_user_credentials(self, username: str, password: str) -> bool:
        """
        Check if a user with the given username and password exists.

        Parameters:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            bool: True if a user with the provided credentials exists, False otherwise.
        """
        # Query the database to find a user with the given username and password
        user = self.db.query(User).filter(User.username == username, User.password == password).first()
        # If user is not None, it means a user with the provided credentials exists
        return user is not None

    def is_manager_by_username_and_password(self, username: str, password: str) -> bool:
        """
        Check if a user with the given username and password is a manager.

        Parameters:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            bool: True if the user with the provided credentials is a manager, False otherwise.
        """
        # Query the database to find a user with the given username and password
        user = self.db.query(User).filter(User.username == username, User.password == password).first()

        # Check if the user exists and is a manager
        return user is not None and user.isManager

    def get_user_by_username_and_password(self, username: str, password: str):
        """
        Retrieves a user by username and password.

        Parameters:
            username (str): The username of the user to retrieve.
            password (str): The password of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        # Query the database to find a user with the given username and password
        return self.db.query(User).filter(User.username == username, User.password == password).first()

    def get_user_by_username(self, username: str):
        """
        Retrieves a user by username.

        Parameters:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        # Query the database to find a user with the given username and password
        return self.db.query(User).filter(User.username == username).first()

    def custom_operation_for_test_only(self):
        return 30

    def approve_user(self, user_name: str):
        """
        Approve a user by setting isApproval to True.

        Parameters:
            user_name (str): The user_name of the user to approve.
        """
        # Retrieve the user by ID
        user = self.get_user_by_username(user_name)
        # If user is found, update isApproval attribute and commit changes
        if user:
            user.isApproval = True
            self.db.commit()

    def get_user_by_name(self, name: str):
        """
        Retrieves a user by name.

        Parameters:
            name (str): The name of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        return self.db.query(User).filter(User.name == name).first()

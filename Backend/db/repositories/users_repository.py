from sqlalchemy.orm import Session
from Backend.db.models import User
from Backend.db.repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, User)
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

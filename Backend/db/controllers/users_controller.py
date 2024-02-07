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

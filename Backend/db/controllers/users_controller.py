from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.users_repository import UsersRepository
from Backend.db.services.users_service import UsersService


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

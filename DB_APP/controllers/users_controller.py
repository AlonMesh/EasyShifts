from __future__ import annotations
from sqlalchemy.orm import Session
from DB_APP.controllers.base_controller import BaseController
from DB_APP.db.repositories.users_repository import UsersRepository
from DB_APP.db.services.users_service import UsersService


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
        super().__init__(db, UsersRepository, UsersService)
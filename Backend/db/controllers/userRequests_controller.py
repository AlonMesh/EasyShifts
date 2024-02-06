from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.userRequests_repository import UserRequestsRepository
from Backend.db.services.userRequests_service import UserRequestsService


class UserRequestsController(BaseController):
    """
    UserRequestsController Class

    Controller class for managing UserRequest entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the UserRequestsController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        super().__init__(db, UserRequestsRepository, UserRequestsService)

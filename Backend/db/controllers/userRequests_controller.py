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
        self.repository = UserRequestsRepository(db)
        self.service = UserRequestsService(self.repository)
        super().__init__(self.repository, self.service)

    def get_request_by_userid(self, id: int):
        """
        Retrieves a user request by userid.

        Parameters:
            id (int): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """

        return self.service.get_request_by_userid(id)

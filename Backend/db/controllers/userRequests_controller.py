from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.controllers.users_controller import UsersController
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

    def get_request_by_userid(self, user_id: str):
        """
        Retrieves a user request by userid.

        Parameters:
            user_id (int): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """
        user_controller = UsersController(self.repository.db)
        if user_controller.get_entity(user_id).isApproval:
            request = self.service.get_request_by_userid(user_id)
            return request
        return None

    def get_request_content_by_user_id_between_datetimes(self, user_id: str, start_datetime, end_datetime):
        """
        Retrieves a user request by userid after a certain datetime.

        Parameters:
            user_id (int): the user id in db
            start_datetime: the start datetime to check
            end_datetime: the end datetime to check

        Returns: The request content if found, None otherwise.
        """
        return self.service.get_request_content_by_user_id_between_datetimes(user_id, start_datetime, end_datetime)

    def get_request_id_by_userid(self, user_id: str) -> int:
        """
        Retrieves the ID of the user request by user ID.

        Parameters:
            user_id (str): The user ID.

        Returns:
            int: The ID of the user request if found, None otherwise.
        """
        return self.repository.get_request_id_by_userid(user_id)
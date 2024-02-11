from sqlalchemy.orm import Session
from Backend.db.models import UserRequest
from Backend.db.repositories.base_repository import BaseRepository


class UserRequestsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, UserRequest)

    def get_request_by_userid(self, id: int):
        """
        Retrieves a user request by userid.

        Parameters:
            id (int): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """
        return self.db.query(UserRequest).filter(UserRequest.id == id).first()

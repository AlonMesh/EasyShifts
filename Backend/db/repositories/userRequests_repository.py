from sqlalchemy.orm import Session
from Backend.db.models import UserRequest
from Backend.db.repositories.base_repository import BaseRepository


class UserRequestsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, UserRequest)

    def get_request_by_userid(self, id: str):
        """
        Retrieves a user request by userid.

        Parameters:
            id (str): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """
        return self.db.query(UserRequest).filter(UserRequest.id == id).first()

    def get_request_id_by_userid(self, user_id: int) -> int:
        """
        Retrieves the ID of the user request by user ID.

        Parameters:
            user_id (int): The user ID.

        Returns:
            int: The ID of the user request if found, None otherwise.
        """
        user_request = self.db.query(UserRequest).filter(UserRequest.id == user_id).first()
        if user_request:
            return user_request.id
        return None
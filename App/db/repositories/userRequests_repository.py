from sqlalchemy.orm import Session
from Backend.db.models import UserRequest
from Backend.db.repositories.base_repository import BaseRepository


class UserRequestsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, UserRequest)

from sqlalchemy.orm import Session
from App.db.models import UserRequest
from App.db.repositories.base_repository import BaseRepository


class UserRequestsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, UserRequest)

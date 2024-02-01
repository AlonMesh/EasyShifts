from sqlalchemy.orm import Session
from DB_APP.db.models import UserRequest
from DB_APP.db.repositories.base_repository import BaseRepository


class UserRequestsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, UserRequest)

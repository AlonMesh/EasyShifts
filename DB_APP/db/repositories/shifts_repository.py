from sqlalchemy.orm import Session
from DB_APP.db.models import Shift
from DB_APP.db.repositories.base_repository import BaseRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

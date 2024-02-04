from sqlalchemy.orm import Session
from App.db.models import Shift
from App.db.repositories.base_repository import BaseRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

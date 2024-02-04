from sqlalchemy.orm import Session
from Backend.db.models import Shift
from Backend.db.repositories.base_repository import BaseRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

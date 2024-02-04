from sqlalchemy.orm import Session
from Backend.db.models import ShiftWorker
from Backend.db.repositories.base_repository import BaseRepository


class ShiftWorkersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShiftWorker)

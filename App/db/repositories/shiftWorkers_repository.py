from sqlalchemy.orm import Session
from App.db.models import ShiftWorker
from App.db.repositories.base_repository import BaseRepository


class ShiftWorkersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShiftWorker)

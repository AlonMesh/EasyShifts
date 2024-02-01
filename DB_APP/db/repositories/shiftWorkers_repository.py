from sqlalchemy.orm import Session
from DB_APP.db.models import ShiftWorker
from DB_APP.db.repositories.base_repository import BaseRepository


class ShiftWorkersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShiftWorker)

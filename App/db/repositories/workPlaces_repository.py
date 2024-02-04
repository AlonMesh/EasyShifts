from sqlalchemy.orm import Session
from Backend.db.models import WorkPlace
from Backend.db.repositories.base_repository import BaseRepository


class WorkPlacesRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, WorkPlace)

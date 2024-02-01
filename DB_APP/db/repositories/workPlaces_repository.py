from sqlalchemy.orm import Session
from DB_APP.db.models import WorkPlace
from DB_APP.db.repositories.base_repository import BaseRepository


class WorkPlacesRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, WorkPlace)

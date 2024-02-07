from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.workPlaces_repository import WorkPlacesRepository
from Backend.db.services.workPlaces_service import WorkPlacesService


class WorkPlacesController(BaseController):
    """
    WorkPlacesController Class

    Controller class for managing workPlaces entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the WorkPlacesController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        self.repository = WorkPlacesRepository(db)
        self.service = WorkPlacesService(self.repository)
        super().__init__(self.repository, self.service)

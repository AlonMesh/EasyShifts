from __future__ import annotations
from sqlalchemy.orm import Session
from App.controllers.base_controller import BaseController
from App.db.repositories.workPlaces_repository import WorkPlacesRepository
from App.db.services.workPlaces_service import WorkPlacesService


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
        super().__init__(db, WorkPlacesRepository, WorkPlacesService)

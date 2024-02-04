from __future__ import annotations
from sqlalchemy.orm import Session
from App.controllers.base_controller import BaseController
from App.db.repositories.shiftWorkers_repository import ShiftWorkersRepository
from App.db.services.shiftWorkers_service import ShiftWorkersService


class ShiftWorkersController(BaseController):
    """
    ShiftWorkersController Class

    Controller class for managing ShiftWorker entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the ShiftWorkersController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        super().__init__(db, ShiftWorkersRepository, ShiftWorkersService)

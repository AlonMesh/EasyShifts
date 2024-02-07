from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.shiftWorkers_repository import ShiftWorkersRepository
from Backend.db.services.shiftWorkers_service import ShiftWorkersService


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
        self.repository = ShiftWorkersRepository(db)
        self.service = ShiftWorkersService(self.repository)
        super().__init__(self.repository, self.service)

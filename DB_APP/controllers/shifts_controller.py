from __future__ import annotations
from sqlalchemy.orm import Session
from DB_APP.controllers.base_controller import BaseController
from DB_APP.db.repositories.shifts_repository import ShiftsRepository
from DB_APP.db.services.shifts_service import ShiftsService


class ShiftsController(BaseController):
    """
    ShiftsController Class

    Controller class for managing shift entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the ShiftsController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        super().__init__(db, ShiftsRepository, ShiftsService)

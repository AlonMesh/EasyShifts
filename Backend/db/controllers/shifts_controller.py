from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.shifts_repository import ShiftsRepository
from Backend.db.services.shifts_service import ShiftsService


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
        self.repository = ShiftsRepository(db)
        self.service = ShiftsService(self.repository)
        super().__init__(self.repository, self.service)

    def get_shift_date_by_shift_id(self, shift_id: int):
        """
        Retrieves the shift's date by its ID.

        Parameters:
            shift_id (int): ID of the shift to retrieve the date for.

        Returns:
             The date of the shift.

        Raises:
            NoResultFound: If the shift with the specified ID is not found.
        """
        return self.service.get_shift_date_by_shift_id(shift_id)

    def get_all_shifts_of_worker_since_date(self, date: datetime):
        """
        Retrieves all shifts of a worker since a given date.

        Parameters:
            date (datetime): Date to retrieve the shifts since.

        Returns:
            List of shifts of the worker since the given date.
        """
        try:
            shifts = self.repository.get_all_shifts_since_date(date)
            return shifts
        except NoResultFound:
            return None  # It's okay to assume that the worker has no shifts since the given date.

    def get_all_shifts_since_date_for_given_worker(self, date: datetime, worker_id: int):
        """
        Retrieves all shifts of a worker since a given date.

        Args:
            date (datetime): Date to retrieve the shifts since.
            worker_id (int): ID of the worker to retrieve shifts for.

        Returns: List of shifts of the worker since the given date.
        """
        return self.repository.get_all_shifts_since_date_for_given_worker(date, worker_id)


from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from Backend.db.models import Shift
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.repositories.shiftWorkers_repository import ShiftWorkersRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

    def get_all_shifts_since_date(self, date: datetime):
        """
        Retrieves all shifts of a worker since a given date.

        Parameters:
            date (datetime): Date to retrieve the shifts since.

        Returns:
            List of shifts of the worker since the given date.
        """
        return self.db.query(Shift).filter(
            Shift.shiftDate >= date
        ).all()

    def get_all_shifts_since_date_for_given_worker(self, date: datetime, worker_id: int) -> List[Shift]:
        """
        Retrieves all shifts of a worker since a given date.
        Args:
            date (datetime): Date to retrieve the shifts since.
            worker_id (int): ID of the worker to retrieve shifts for.

        Returns: List of shifts of the worker since the given date.
        """
        # Reuse the get_all_shifts_since_date function
        shifts = self.get_all_shifts_since_date(date)

        # Get the shift workers repository
        shift_workers_repository = ShiftWorkersRepository(self.db)

        # Filter shifts based on the given worker ID
        shifts_for_worker = [shift for shift in shifts if
                             shift_workers_repository.is_shift_assigned_to_worker(shift.id, worker_id)]
        return shifts_for_worker

    def get_all_shifts_since_date_for_given_workplace(self, date: datetime, workplace_id: int) -> List[Shift]:
        """
        Retrieves all shifts of a workplace since a given date.
        Args:
            date (datetime): Date to retrieve the shifts since.
            workplace_id (int): ID of the workplace to retrieve shifts for.

        Returns: List of shifts of the workplace since the given date.
        """
        # Reuse the get_all_shifts_since_date function
        shifts = self.get_all_shifts_since_date(date)

        # Filter shifts based on the given workplace ID
        shifts_for_workplace = [shift for shift in shifts if shift.workPlaceID == workplace_id]
        return shifts_for_workplace

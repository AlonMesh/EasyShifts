from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.models import Shift
from Backend.db.repositories.base_repository import BaseRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

    def get_shift_date_by_shift_id(self, shift_id: int) -> datetime:
        """
        Retrieves the shift date by shift ID.

        Parameters:
            shift_id (int): ID of the shift to retrieve the date for.

        Returns:
             The date of the shift.

        Raises:
            NoResultFound: If the shift with the specified ID is not found.
        """
        try:
            shift = self.db.query(Shift).filter(self.entity_type.id == shift_id).one()
            return shift.shiftDate
        except NoResultFound:
            raise NoResultFound(f"No shift found with ID {shift_id}")

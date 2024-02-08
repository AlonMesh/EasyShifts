from typing import List, Type
from sqlalchemy.orm import Session
from Backend.db.models import ShiftWorker
from Backend.db.repositories.base_repository import BaseRepository


class ShiftWorkersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShiftWorker)

    def get_shifts_by_shift_id(self, shift_id: int) -> list[Type[ShiftWorker]]:
        """
        Retrieves all shift workers by shift ID.

        Parameters:
            shift_id (int): ID of the shift to retrieve workers for.

        Returns:
            List[ShiftWorker]: A list of all shift workers for the shift.
        """
        return self.db.query(ShiftWorker).filter(ShiftWorker.ShiftID == shift_id).all()

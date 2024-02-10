from typing import List, Type
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.models import ShiftWorker
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.repositories.users_repository import UsersRepository


class ShiftWorkersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShiftWorker)

    def get_entity_shift_worker(self, shift_id: int, user_id: int) -> Type[ShiftWorker]:
        """
        Retrieves a shift worker by shift ID and user ID.

        Args:
            shift_id (int): ID of the shift
            user_id (int): ID of the worker

        Returns: An entity of ShiftWorker

        """
        entity = self.db.query(ShiftWorker).filter(self.entity_type.shiftID == shift_id,
                                                   self.entity_type.userID == user_id).first()
        if entity is None:
            raise NoResultFound(f"No shift worker found with shiftID {shift_id} and userID {user_id}")
        return entity

    def delete_entity_shift_worker(self, shift_id: int, user_id: int):
        db_entity = self.get_entity_shift_worker(shift_id, user_id)

        if db_entity is None:
            raise NoResultFound(f"No shift worker found with shiftID {shift_id} and userID {user_id}")

        self.db.delete(db_entity)
        self.db.commit()

    def get_worker_shifts_by_worker_id(self, worker_id: int) -> List[ShiftWorker]:
        """
        Retrieves all shifts for a worker by worker ID.

        Parameters:
            worker_id (int): ID of the worker to retrieve shifts for.

        Returns:
            List[ShiftWorker]: A list of all shifts for the worker.
        """
        return self.db.query(ShiftWorker).filter(ShiftWorker.userID == worker_id).all()

    def get_shift_workers_by_shift_id(self, shift_id: int) -> List[ShiftWorker]:
        """
        Retrieves all workers for a shift by shift ID.

        Parameters:
            shift_id (int): ID of the shift to retrieve workers for.

        Returns:
            List[ShiftWorker]: A list of all workers for the shift.
        """
        return self.db.query(self.entity_type).filter(self.entity_type.shiftID == shift_id).all()

    def is_shift_assigned_to_worker(self, shift_id: int, worker_id: int) -> bool:
        """
        Checks if a shift is assigned to a worker.

        Parameters:
            shift_id (int): ID of the shift to check.
            worker_id (int): ID of the worker to check.

        Returns:
            bool: True if the shift is assigned to the worker, False otherwise.
        """

        # Check if the user exists in the database
        user_repository = UsersRepository(self.db)
        user_repository.get_entity(worker_id)  # Raises NoResultFound if the user is not found

        # Check if the shift is assigned to the worker
        return self.db.query(ShiftWorker).filter(
            ShiftWorker.shiftID == shift_id,
            ShiftWorker.userID == worker_id
        ).first() is not None

    def convert_shift_workers_by_shift_id_to_client(self, shift_id) -> list[str]:
        """
        Retrieves all workers for a shift by shift ID.
        Args:
            shift_id (int): ID of the shift to retrieve workers for.

        Returns:
            List[str]: A list of all workers for the shift.
        """
        users_repository = UsersRepository(self.db)
        workers = self.get_shift_workers_by_shift_id(shift_id)
        return [users_repository.get_entity(worker.userID).name for worker in workers]

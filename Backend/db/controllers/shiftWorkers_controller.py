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

    def get_entity_shift_worker(self, shift_id: int, user_id: int):
        """
        Retrieves a shift worker by shift ID and user ID.

        Args:
            shift_id (int): ID of the shift
            user_id (int): ID of the worker

        Returns: An entity of ShiftWorker

        """
        return self.repository.get_entity_shift_worker(shift_id, user_id)

    def delete_entity_shift_worker(self, shift_id: int, user_id: int):
        """
        Deletes a shift worker by shift ID and user ID.

        Args:
            shift_id (int): ID of the shift
            user_id (int): ID of the worker

        """
        self.repository.delete_entity_shift_worker(shift_id, user_id)

    def get_worker_shifts_by_worker_id(self, worker_id: int):
        """
        Retrieves all shifts for a worker by worker ID.
        Args:
            worker_id (int): ID of the worker to retrieve shifts for.

        Returns:
            List[ShiftWorker]: A list of all shifts for the worker.
        """
        return self.repository.get_worker_shifts_by_worker_id(worker_id)

    def get_shift_workers_by_shift_id(self, shift_id: int):
        """
        Retrieves all workers for a shift by shift ID.
        Args:
            shift_id (int): ID of the shift to retrieve workers for.

        Returns:
            List[ShiftWorker]: A list of all workers for the shift.
        """
        return self.repository.get_shift_workers_by_shift_id(shift_id)

    def is_shift_assigned_to_worker(self, shift_id: int, worker_id: int):
        """
        Checks if a shift is assigned to a worker.
        Args:
            shift_id (int): ID of the shift
            worker_id (int): ID of the worker

        Returns:
            bool: True if the shift is assigned to the worker, False otherwise.
        """
        return self.repository.is_shift_assigned_to_worker(shift_id, worker_id)
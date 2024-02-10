from __future__ import annotations
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.repositories.workPlaces_repository import WorkPlacesRepository
from Backend.db.services.workPlaces_service import WorkPlacesService

from typing import List, Tuple  # Importing List and Tuple from typing module


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
        self.repository = WorkPlacesRepository(db)
        self.service = WorkPlacesService(self.repository)
        super().__init__(self.repository, self.service)

    def get_active_workers_by_workplace_id(self, workplace_id: int):
        """
        Retrieves the names and IDs of all active workers in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Utilize the service method to get active workers by workplace ID
        return self.service.get_active_workers_by_workplace_id(workplace_id)

    def get_active_workers_for_user(self, user_id: int) -> List[Tuple[int, str]]:
        """
        Retrieves the names and IDs of all active workers in the workplace where the specified user works.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Retrieve the workplace ID for the specified user
        workplace_id = self.repository.get_workplace_id_by_userid(user_id)

        if workplace_id is not None:
            # Utilize the service method to get active workers by workplace ID
            return self.service.get_active_workers_by_workplace_id(workplace_id)
        else:
            # If the user does not work in any workplace, return an empty list
            return []
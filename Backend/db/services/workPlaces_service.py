from Backend.db.repositories.workPlaces_repository import WorkPlacesRepository
from Backend.db.services.base_service import BaseService
from typing import List, Tuple
from Backend.db.models import WorkPlace, User


class WorkPlacesService(BaseService):
    """
    Service class for handling complexes operations.
    """

    def __init__(self, repository: WorkPlacesRepository):
        """
        Initializes the UsersService with a user repository.

        Parameters:
            repository: An instance of WorkPlacesRepository.
        """
        super().__init__(repository)

    def custom_operation(self):
        """
        Placeholder for a custom operation.
        Actual implementation is not provided yet.
        """
        pass

    def get_active_workers_by_workplace_id(self, user_id: int) -> List[Tuple[int, str]]:
        """
        Retrieves the IDs and names of all active workers in the workplace of the specified user.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Get the workplace ID for the specified user
        workplace_id = self.repository.get_workplace_id_by_user_id(user_id)

        if workplace_id is not None:
            # Get all active users in the workplace by workplace ID
            active_users = self.repository.get_active_users_by_workplace_id(workplace_id)

            # Construct a list of tuples containing worker IDs and names
            active_workers = [(user.id, user.name) for user in active_users]
            return active_workers
        else:
            # If the user does not work in any workplace, return an empty list
            return []

        return worker_info

    def get_active_approved_workers_by_workplace_id(self, workplace_id: int) -> List[Tuple[int, str]]:
        """
        Retrieves the IDs and names of all active workers with approval in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Get all active users in the specified workplace
        active_users = self.repository.get_active_users_by_workplace_id(workplace_id)

        # Filter active users who have approval
        approved_users = [(user.id, user.name) for user in active_users if user.isApproval]

        return approved_users

    def get_active_unapproved_workers_by_workplace_id(self, workplace_id: int) -> List[Tuple[int, str]]:
        """
        Retrieves the IDs and names of all active workers without approval in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Get all active users in the specified workplace
        active_users = self.repository.get_active_users_by_workplace_id(workplace_id)

        # Filter active users who do not have approval
        unapproved_users = [(user.id, user.name) for user in active_users if not user.isApproval]

        return unapproved_users

    def get_workplace_id_by_worker_id(self, user_id: int) -> int:
        """
        Retrieves the workplace ID for the specified user.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            int | None: The workplace ID if the user works in a workplace, else None.
        """
        return self.repository.get_workplace_by_worker_id(user_id).id

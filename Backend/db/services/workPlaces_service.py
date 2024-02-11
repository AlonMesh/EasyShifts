from Backend.db.repositories.workPlaces_repository import WorkPlacesRepository
from Backend.db.services.base_service import BaseService


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

    def get_active_workers_by_workplace_id(self, workplace_id: int):
        """
        Retrieves the names and IDs of all active workers in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing worker IDs and names.
        """
        # Get active users by workplace ID from the repository
        active_users = self.repository.get_active_users_by_workplace_id(workplace_id)

        # Extract worker IDs and names from active users
        worker_info = [(user.id, user.name) for user in active_users]

        return worker_info

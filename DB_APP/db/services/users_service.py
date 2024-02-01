from DB_APP.db.repositories.users_repository import UsersRepository
from DB_APP.db.services.base_service import BaseService


class UsersService(BaseService):
    """
    Service class for handling complexes operations.
    """

    def __init__(self, repository: UsersRepository):
        """
        Initializes the UsersService with a user repository.

        Parameters:
            repository: An instance of UsersRepository.
        """
        super().__init__(repository)

    def custom_operation(self):
        """
        Placeholder for a custom operation.
        Actual implementation is not provided yet.
        """
        pass

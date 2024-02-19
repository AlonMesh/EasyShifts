from Backend.db.repositories.userRequests_repository import UserRequestsRepository
from Backend.db.services.base_service import BaseService


class UserRequestsService(BaseService):
    """
    Service class for handling complexes operations.
    """

    def __init__(self, repository: UserRequestsRepository):
        """
        Initializes the UsersService with a user repository.

        Parameters:
            repository: An instance of UserRequestsRepository.
        """
        super().__init__(repository)

    def custom_operation(self):
        """
        Placeholder for a custom operation.
        Actual implementation is not provided yet.
        """
        pass

    def get_request_by_userid(self, id: int):
        """
        Retrieves a user request by userid.

        Parameters:
            id (int): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """

        user_request = self.repository.get_request_by_userid(id)
        if user_request:
            return user_request.requests
        return None

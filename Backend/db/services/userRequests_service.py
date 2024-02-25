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

    def get_request_by_userid(self, user_id: str):
        """
        Retrieves a user request by userid.

        Parameters:
            user_id (str): the user id in db

        Returns:
            UserRequest: The user-request object if found, None otherwise.
        """

        user_request = self.repository.get_request_by_userid(user_id)
        if user_request:
            return user_request.requests
        return None

    def get_request_content_by_user_id_between_datetimes(self, user_id: str, start_datetime, end_datetime):
        """
        Retrieves a user request by userid between two datetimes.

        Parameters:
            user_id (int): the user id in db
            start_datetime: the start datetime to check
            end_datetime: the end datetime to check

        Returns:
            UserRequest: The request content if found, None otherwise.
        """
        # Get the user request
        user_request = self.get_request_by_userid(user_id)

        # Check if the user request is between the start and end datetimes
        if user_request and start_datetime <= user_request.modifyAt <= end_datetime:
            return user_request.requests

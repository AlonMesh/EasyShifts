class UserSession:
    """
    Represents an active user session in the site.

    Attributes:
        _user_id (int): The user's ID.
        _is_manager (bool): True if the user is a manager, False if a worker.
    """

    def __init__(self, user_id: int, is_manager: bool):
        """
        Initializes a UserSession object.

        Parameters:
            user_id (int): The user's ID.
            is_manager (bool): True if the user is a manager, False if a worker.
        """
        self._user_id = user_id
        self._is_manager = is_manager

    def can_access_manager_page(self):
        """
        Checks if the user can access manager-specific pages.

        Returns:
            bool: True if the user is a manager, False otherwise.
        """
        return self._is_manager

    def can_access_worker_page(self):
        """
        Checks if the user can access worker-specific pages.

        Returns:
            bool: True if the user is a worker, False otherwise.
        """
        return not self._is_manager

    @property
    def get_id(self):
        """
        Retrieves the user's ID.

        Returns:
            int: The user's ID.
        """
        return self._user_id

from App.db.repositories.base_repository import BaseRepository


class BaseService:
    """
    A generic service class providing common operations for services.

    Attributes:
        repository (BaseRepository): An instance of BaseRepository for data access.
    """

    def __init__(self, repository: BaseRepository):
        """
        Initializes the BaseService with a repository.

        Parameters:
            repository (BaseRepository): An instance of BaseRepository.
        """
        self.repository = repository

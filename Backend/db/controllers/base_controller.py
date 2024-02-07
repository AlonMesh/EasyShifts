from sqlalchemy.orm import Session
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.services.base_service import BaseService
from typing import Type, TypeVar

EntityType = TypeVar("EntityType", bound=BaseRepository)


class BaseController:
    """
    A generic controller class providing common operations for controllers.
    """

    def __init__(self, repository, service):
        """
        Initializes the BaseController with a repository and service.

        Parameters:
            repository: An instance of the repository type for database interactions.
            service: An instance of the service type for handling complex operations.
        """
        self.repository = repository
        self.service = service

    def create_entity(self, entity_data: dict) -> EntityType:
        """
        Creates a new entity using the associated repository.

        Parameters:
            entity_data (dict): Dictionary containing entity data.

        Returns:
            EntityType: The created entity.
        """
        return self.repository.create_entity(entity_data)

    def get_entity(self, entity_id: int) -> EntityType:
        """
        Retrieves an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to retrieve.

        Returns:
            EntityType: The retrieved entity if found, else None.
        """
        return self.repository.get_entity(entity_id)

    def get_all_entities(self) -> list[EntityType]:
        """
        Retrieves all entities using the associated repository.

        Returns:
            List[EntityType]: A list of all entities.
        """
        return self.repository.get_all_entities()

    def update_entity(self, entity_id: int, updated_data: dict) -> EntityType:
        """
        Updates an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to update.
            updated_data (dict): Dictionary containing updated entity data.

        Returns:
            EntityType: The updated entity if found, else None.
        """
        return self.repository.update_entity(entity_id, updated_data)

    def delete_entity(self, entity_id: int) -> EntityType:
        """
        Deletes an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to delete.

        Returns:
            EntityType: The deleted entity if found, else None.
        """
        return self.repository.delete_entity(entity_id)

    def perform_custom_operation(self) -> any:
        """
        Performs a custom operation using the associated service.

        Returns:
            Any: The result of the custom operation.
        """
        # service = self.service_type(self.repository_type(self.db))
        # return service.custom_operation()
        pass

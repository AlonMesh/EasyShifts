from sqlalchemy.orm import Session
from DB_APP.db.repositories.base_repository import BaseRepository
from DB_APP.db.services.base_service import BaseService
from typing import Type, TypeVar

EntityType = TypeVar("EntityType", bound=BaseRepository)


class BaseController:
    """
    A generic controller class providing common operations for controllers.

    Attributes:
        db (Session): SQLAlchemy Session for database interactions.
        repository_type (Type[BaseRepository]): Type of the repository associated with the controller.
        service_type (Type[BaseService]): Type of the service associated with the controller.
    """

    def __init__(self, db: Session, repository_type: Type[BaseRepository], service_type: Type[BaseService]):
        """
        Initializes the BaseController with a database session, repository type, and service type.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
            repository_type (Type[BaseRepository]): Type of the repository associated with the controller.
            service_type (Type[BaseService]): Type of the service associated with the controller.
        """
        self.db = db
        self.repository_type = repository_type
        self.service_type = service_type

    def create_entity(self, entity_data: dict) -> EntityType:
        """
        Creates a new entity using the associated repository.

        Parameters:
            entity_data (dict): Dictionary containing entity data.

        Returns:
            EntityType: The created entity.
        """
        repository = self.repository_type(self.db)
        return repository.create_entity(entity_data)

    def get_entity(self, entity_id: int) -> EntityType:
        """
        Retrieves an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to retrieve.

        Returns:
            EntityType: The retrieved entity if found, else None.
        """
        repository = self.repository_type(self.db)
        return repository.get_entity(entity_id)

    def get_all_entities(self) -> list[EntityType]:
        """
        Retrieves all entities using the associated repository.

        Returns:
            List[EntityType]: A list of all entities.
        """
        repository = self.repository_type(self.db)
        return repository.get_all_entities()

    def update_entity(self, entity_id: int, updated_data: dict) -> EntityType:
        """
        Updates an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to update.
            updated_data (dict): Dictionary containing updated entity data.

        Returns:
            EntityType: The updated entity if found, else None.
        """
        repository = self.repository_type(self.db)
        return repository.update_entity(entity_id, updated_data)

    def delete_entity(self, entity_id: int) -> EntityType:
        """
        Deletes an entity using the associated repository.

        Parameters:
            entity_id (int): ID of the entity to delete.

        Returns:
            EntityType: The deleted entity if found, else None.
        """
        repository = self.repository_type(self.db)
        return repository.delete_entity(entity_id)

    def perform_custom_operation(self) -> any:
        """
        Performs a custom operation using the associated service.

        Returns:
            Any: The result of the custom operation.
        """
        # service = self.service_type(self.repository_type(self.db))
        # return service.custom_operation()
        pass

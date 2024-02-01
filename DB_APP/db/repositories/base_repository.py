from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from typing import Type, TypeVar

Base = declarative_base()
EntityType = TypeVar("EntityType", bound=DeclarativeMeta)


class BaseRepository:
    """
    A generic repository class providing common CRUD operations for database entities.

    Attributes:
        db (Session): SQLAlchemy Session for database interactions.
        entity_type (Type[EntityType]): Type of the entity to be managed by the repository.
    """
    def __init__(self, db: Session, entity_type: Type[EntityType]):
        """
        Initializes the BaseRepository with a database session and entity type.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
            entity_type (Type[EntityType]): Type of the entity to be managed by the repository.
        """
        self.db = db
        self.entity_type = entity_type

    def create_entity(self, entity_data: dict) -> EntityType:
        """
        Creates a new entity in the database.

        Parameters:
            entity_data (dict): Dictionary containing entity data.

        Returns:
            EntityType: The created entity.
        """
        # Creating an entity based on a dict data
        db_entity = self.entity_type(**entity_data)

        # Add that entity to the db, commit it and refresh it
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)

        # Return the created entity
        return db_entity

    def get_entity(self, entity_id: int) -> EntityType:
        """
        Retrieves an entity by its ID.

        Parameters:
            entity_id (int): ID of the entity to retrieve.

        Returns:
            EntityType: The retrieved entity if found, else None.
        """
        return self.db.query(self.entity_type).filter(self.entity_type.id == entity_id).first()

    def get_all_entities(self) -> list[EntityType]:
        """
        Retrieves all entities from the database.

        Returns:
            List[EntityType]: A list of all entities.
        """
        return self.db.query(self.entity_type).all()

    def update_entity(self, entity_id: int, updated_data: dict) -> EntityType | None:
        """
        Updates an entity in the database.

        Parameters:
            entity_id (int): ID of the entity to update.
            updated_data (dict): Dictionary containing updated entity data.

        Returns:
            EntityType: The updated entity if found, else None.
        """
        # Get a reference to entity in the db
        db_entity = self.get_entity(entity_id)

        # If it exists, update it
        if db_entity:
            for key, value in updated_data.items():
                setattr(db_entity, key, value)
            self.db.commit()
            self.db.refresh(db_entity)

        # TODO: Raise error if it doesn't exist

        return db_entity

    def delete_entity(self, entity_id: int) -> EntityType | None:
        """
        Deletes an entity from the database.

        Parameters:
            entity_id (int): ID of the entity to delete.

        Returns:
            EntityType: The deleted entity if found, else None.
        """
        # Get a reference to entity in the db
        db_entity = self.get_entity(entity_id)

        # If it exists, update it
        if db_entity:
            self.db.delete(db_entity)
            self.db.commit()

        # TODO: Raise error if it doesn't exist

        return db_entity

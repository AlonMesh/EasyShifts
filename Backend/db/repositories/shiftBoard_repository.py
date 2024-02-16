from typing import Type
from sqlalchemy import Date
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.models import ShiftBoard


class ShiftBoardRepository:
    def __init__(self, db: Session):
        self.db = db
        self.shiftBoard = ShiftBoard

    def create_entity(self, entity_data: dict):
        """
        Creates a new entity in the database.

        Parameters:
            entity_data (dict): Dictionary containing entity data.

        Returns:
            EntityType: The created entity.
        """
        # Creating an entity based on a dict data
        db_entity = self.shiftBoard(**entity_data)

        # Add that entity to the db, commit it and refresh it
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)

        # Return the created entity
        return db_entity

    def get_entity(self, week_start_day: Date, workplace_id: str) -> Type[ShiftBoard]:
        """
        Retrieves an entity by its ID.

        Parameters:
            week_start_day (Date): Date of the week.
            workplace_id (str): ID of the workplace.

        Raises:
            NoResultFound: If the entity with the specified ID is not found.

        Returns:
            EntityType: The retrieved entity if found.
        """
        entity = self.db.query(self.shiftBoard).filter(
            self.shiftBoard.weekStartDate == week_start_day,
            self.shiftBoard.workplaceID == workplace_id
        ).first()

        if entity is None:
            raise NoResultFound(f'Shiftboard starts at {week_start_day} with workplace_id {workplace_id} not found')

        return entity

    def get_all_entities(self) -> list[Type[ShiftBoard]]:
        """
        Retrieves all entities from the database.

        Returns:
            List of all entities.
        """
        return self.db.query(self.shiftBoard).all()

    def update_entity(self, week_start_day: Date, workplace_id: str, updated_data: dict) -> Type[ShiftBoard]:
        """
        Updates an entity in the database.

        Parameters:
            week_start_day (Date): Date of the week.
            workplace_id (str): ID of the workplace.
            updated_data (dict): Dictionary containing updated entity data.

        Returns:
            EntityType: The updated entity.
        """
        # Get the entity to update
        entity = self.get_entity(week_start_day, workplace_id)

        # Update the entity with the new data
        for key, value in updated_data.items():
            setattr(entity, key, value)

        # Commit the changes
        self.db.commit()

        # Return the updated entity
        return entity

    def delete_entity(self, week_start_day: Date, workplace_id: str) -> Type[ShiftBoard]:
        """
        Deletes an entity from the database.

        Parameters:
            week_start_day (Date): Date of the week.
            workplace_id (str): ID of the workplace.

        Returns:
            EntityType: The deleted entity.
        """
        # Get the entity to delete
        entity = self.get_entity(week_start_day, workplace_id)

        # Delete the entity
        self.db.delete(entity)
        self.db.commit()

        # Return the deleted entity
        return entity

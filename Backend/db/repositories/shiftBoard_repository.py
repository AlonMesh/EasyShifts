from datetime import timedelta
from typing import Type
from sqlalchemy import Date
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.models import ShiftBoard, ShiftPart
from Backend.config.constants import next_sunday
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shift_for_client


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

        # TODO: first, delete all shifts related to this shift board

        # Get the entity to delete
        entity = self.get_entity(week_start_day, workplace_id)

        # Delete the entity
        self.db.delete(entity)
        self.db.commit()

        # Return the deleted entity
        return entity

    def get_all_shift_boards_by_workplace(self, workplace_id: str) -> list[Type[ShiftBoard]]:
        """
        Retrieves all shift boards from the database by workplace.

        Parameters:
            workplace_id (str): ID of the workplace.

        Returns:
            List of all shift boards.
        """
        return self.db.query(self.shiftBoard).filter(self.shiftBoard.workplaceID == workplace_id).order_by(
            self.shiftBoard.weekStartDate).all()

    def get_content_template_by_preferences(self, preferences, workplace_id) -> dict:
        """
        Generate a content template for a shift board based on preferences.

        Parameters:
            workplace_id:
            preferences (dict): Dictionary containing preferences.
                - number_of_shifts_per_day (int): Number of shifts per day.
                - closed_days (list): List of closed days.

        Returns:
            dict: Content template for a shift board.
        """
        content_template = {}

        # Define the shift parts based on the preferences
        shift_parts = [ShiftPart.Morning, ShiftPart.Noon, ShiftPart.Evening][
                      :preferences.get("number_of_shifts_per_day", 1)]

        # Get the closed days from the preferences
        closed_days = preferences.get("closed_days", [])

        # Creating shift controller
        shift_controller = ShiftsController(self.db)

        # Get the next Sunday date
        next_sunday_date = next_sunday

        for i in range(7):  # Iterate over 7 days of the week
            # Calculate the date for the current day
            current_date = next_sunday_date + timedelta(days=i)

            # Get the day name for the current date
            day_name = current_date.strftime("%A")

            # Initialize shifts for the day
            content_template[day_name] = {}

            for part in shift_parts:
                # If the day is closed, skip the shifts
                if day_name in closed_days:
                    content_template[day_name][part] = "CLOSED"
                    continue  # Skip the shifts

                # Create a shift for the day and part
                shift_data = {
                    "shiftDate": current_date,
                    "shiftPart": part,
                    "workPlaceID": workplace_id
                }

                # Create a shift entity
                shift = shift_controller.create_entity(shift_data)

                # Convert the shift to a client-friendly format
                shift_for_client = convert_shift_for_client(shift, self.db)

                # Get the workers list for the shift
                workers_list = shift_for_client["workers"]

                # Referring the value `workers_list` to the corresponding key in the content_template
                content_template[day_name][part] = workers_list

        return content_template

from __future__ import annotations
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.models import WorkPlace, User
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.controllers.users_controller import UsersController


class WorkPlacesRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, WorkPlace)

    def get_users_by_workplace_id(self, workplace_id: str):
        """
        Retrieves all users working in the specified workplace.

        Parameters:
            workplace_id (str): ID of the workplace.

        Returns:
            list[User]: A list of users working in the specified workplace.
        """
        # Query users by joining WorkPlace and User tables
        return (
            self.db.query(User)
            .join(WorkPlace)
            .filter(WorkPlace.workPlaceID == workplace_id)
            .all()
        )

    def get_active_users_by_workplace_id(self, workplace_id: str):
        """
        Retrieves all active users working in the specified workplace.

        Parameters:
            workplace_id (str): ID of the workplace.

        Returns:
            list[User]: A list of active users working in the specified workplace.
        """
        # Query active users by joining WorkPlace and User tables and filtering by isActive = 1
        return (
            self.db.query(User)
            .join(WorkPlace)
            .filter(WorkPlace.workPlaceID == workplace_id)
            .filter(User.isActive == 1)
            .all()
        )

    def get_workplace_id_by_user_id(self, user_id: str) -> str:
        """
        Retrieves the workplace ID for the specified user.

        Parameters:
            user_id (str): ID of the user.

        Returns:
            str: The workplace ID if the user works in a workplace.

        Raises:
            NoResultFound: If the workplace for the specified user is not found.
        """
        # Query the WorkPlace table to find the workplace associated with the user
        workplace = (
            self.db.query(WorkPlace)
            .filter(WorkPlace.workPlaceID == user_id)  # Assuming id represents user ID in WorkPlace
            .first()
        )

        # Raise an exception if workplace is None
        if workplace is None:
            raise NoResultFound(f"Workplace for user with ID {user_id} not found")

        # Return the workplace ID
        return workplace.workPlaceID

    def get_workplace_by_worker_id(self, user_id: str) -> WorkPlace:
        """
        Retrieves the workplace where the specified user works.

        Parameters:
            user_id (str): ID of the user.

        Raises:
            NoResultFound: If the workplace for the specified user is not found.

        Returns:
            WorkPlace: The workplace where the user works.
        """
        # Query the WorkPlace table to find the workplace associated with the user
        workplace = (
            self.db.query(WorkPlace)
            .filter(WorkPlace.id == user_id)  # Assuming id represents user ID in WorkPlace
            .first()
        )

        # Raise an exception if workplace is None
        if workplace is None:
            raise NoResultFound(f"Workplace for user with ID {user_id} not found")

        # Return the workplace itself
        return workplace

    def get_workplace_name_by_worker_id(self, workplace_id: str) -> str:
        """
        Retrieves the workplace name by ID.

        Parameters:
            workplace_id (str): ID of the workplace.

        Returns:
            str: The workplace name if the workplace exists, None otherwise.
        """
        # Query the WorkPlace table to find the workplace by ID
        result = (
            self.db.query(User, WorkPlace)
            .join(WorkPlace, User.id == WorkPlace.id)
            .filter(User.id == workplace_id)
            .first()
        )

        if result:
            user, workplace = result
            userController = UsersController(self.db)
            return userController.get_name_by_id(workplace.workPlaceID)

    def get_worker_by_name(self, workplace_id, worker_name):
        """
        Retrieves the worker by name.

        Parameters:
            workplace_id (str): ID of the workplace.
            worker_name (str): Name of the worker.

        Returns:
            User: The user with the specified name.
        """
        # Query the User table to find the user by name
        return (
            self.db.query(User)
            .join(WorkPlace)
            .filter(WorkPlace.workPlaceID == workplace_id)
            .filter(User.name == worker_name)
            .first()
        )

    def get_business_id_by_name(self, work_place_name: str) -> int | None:
        """
        Retrieves the business ID based on the provided manager username.

        Parameters:
            work_place_name (str): The username of the manager.

        Returns:
            int | None: The ID of the business if found, else None.
        """
        # Query the Users table to retrieve the user by username
        user_controller = UsersController(self.db)
        user = user_controller.get_entity(user_controller.get_user_id_by_name(work_place_name))
        print(user_controller.get_entity(user.id))

        if user and user.isManager:
            # Assuming the business ID is stored in a field called 'business_id' in the Users table
            return user.id
        else:
            return None





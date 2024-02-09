from sqlalchemy.orm import Session
from Backend.db.models import WorkPlace , User
from Backend.db.repositories.base_repository import BaseRepository


class WorkPlacesRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, WorkPlace)

    def get_users_by_workplace_id(self, workplace_id: int):
        """
        Retrieves all users working in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

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

    def get_active_users_by_workplace_id(self, workplace_id: int):
        """
        Retrieves all active users working in the specified workplace.

        Parameters:
            workplace_id (int): ID of the workplace.

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

    def get_workplace_id_by_userid(self, user_id: int):
        """
        Retrieves the workplace ID for the specified user.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            int | None: The workplace ID if the user works in a workplace, else None.
        """
        # Query the WorkPlace table to find the workplace associated with the user
        workplace = (
            self.db.query(WorkPlace)
            .filter(WorkPlace.id == user_id)  # Assuming id represents user ID in WorkPlace
            .first()
        )

        # Return the workplace ID if found, else None
        return workplace.workPlaceID if workplace else None
from datetime import datetime
from Backend.db.repositories.shifts_repository import ShiftsRepository
from Backend.db.services.base_service import BaseService


class ShiftsService(BaseService):
    """
    Service class for handling complexes operations.
    """

    def __init__(self, repository: ShiftsRepository):
        """
        Initializes the ShiftsService with a shift repository.

        Parameters:
            repository: An instance of ShiftsRepository.
        """
        super().__init__(repository)

    def get_shift_date_by_shift_id(self, shift_id: int) -> datetime:
        """
        Retrieves the shift's date by its ID.

        Parameters:
            shift_id (int): ID of the shift to retrieve the given_date for.

        Returns:
             The date of the shift.

        Raises:
            NoResultFound: If the shift with the specified ID is not found.
        """
        shift = self.repository.get_entity(shift_id)
        return shift.shiftDate



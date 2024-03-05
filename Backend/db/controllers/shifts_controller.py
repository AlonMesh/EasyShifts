from datetime import date, datetime
from sqlalchemy import Date
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.controllers.base_controller import BaseController
from Backend.db.models import Shift
from Backend.db.repositories.shifts_repository import ShiftsRepository
from Backend.db.services.shifts_service import ShiftsService
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController


class ShiftsController(BaseController):
    """
    ShiftsController Class

    Controller class for managing shift entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the ShiftsController with a database session.

        Parameters:
            db (Session): SQLAlchemy Session for database interactions.
        """
        self.repository = ShiftsRepository(db)
        self.service = ShiftsService(self.repository)
        super().__init__(self.repository, self.service)

    def get_shift_date_by_shift_id(self, shift_id: str) -> Date:
        """
        Retrieves the shift's date by its ID.

        Parameters:
            shift_id (str): ID of the shift to retrieve the date for.

        Returns:
             The date of the shift.

        Raises:
            NoResultFound: If the shift with the specified ID is not found.
        """
        return self.service.get_shift_date_by_shift_id(shift_id)

    def get_all_shifts_of_worker_since_date(self, date: date):
        """
        Retrieves all shifts of a worker since a given date.

        Parameters:
            date (date): Date to retrieve the shifts since.

        Returns:
            List of shifts of the worker since the given date.
        """
        try:
            shifts = self.repository.get_all_shifts_since_date(date)
            return shifts
        except NoResultFound:
            return None  # It's okay to assume that the worker has no shifts since the given date.

    def get_all_shifts_since_date_for_given_worker(self, date: date, worker_id: str):
        """
        Retrieves all shifts of a worker since a given date.

        Args:
            date (date): Date to retrieve the shifts since.
            worker_id (str): ID of the worker to retrieve shifts for.

        Returns: List of shifts of the worker since the given date.
        """
        return self.repository.get_all_shifts_since_date_for_given_worker(date, worker_id)

    def get_future_shifts_for_user(self, user_id: str):
        """
        Retrieves all future shifts for the specified user.

        Parameters:
            user_id (str): ID of the user to retrieve shifts for.

        Returns:
            List of future shifts for the specified user.
        """
        # This method is just a wrapper around the get_all_shifts_since_date_for_given_worker method
        return self.get_all_shifts_since_date_for_given_worker(datetime.now(), user_id)

    def get_all_shifts_since_date_for_given_workplace(self, given_date: date, workplace_id: str):
        """
        Retrieves all shifts of a workplace since a given date.

        Args:
            given_date (date): Date to retrieve the shifts since.
            workplace_id (str): ID of the workplace to retrieve shifts for.

        Returns: List of shifts of the workplace since the given date.
        """
        return self.repository.get_all_shifts_since_date_for_given_workplace(given_date, workplace_id)

    def get_all_shifts_between_dates_for_given_workplace(self, start_date: date, end_date: date, workplace_id: str):
        """
        Retrieves all shifts of a workplace between two given dates.

        Args:
            start_date (date): Start date to retrieve the shifts from.
            end_date (date): End date to retrieve the shifts until.
            workplace_id (str): ID of the workplace to retrieve shifts for.

        Returns: List of shifts of the workplace between the given dates.
        """
        return self.repository.get_all_shifts_between_dates_for_given_workplace(start_date, end_date, workplace_id)

    def get_future_shifts_for_workplace(self, workplace_id: str):
        """
        Retrieves all future shifts for the specified workplace.

        Parameters:
            workplace_id (str): ID of the workplace to retrieve shifts for.

        Returns:
            List of future shifts for the specified workplace.
        """
        # This method is just a wrapper around the get_all_shifts_since_date_for_given_workplace method
        return self.get_all_shifts_since_date_for_given_workplace(datetime.now(), workplace_id)

    def get_shift_id_by_day_and_part_and_workplace(self, day: str, part: str, workplace: int):
        return self.service.get_shift_id_by_day_and_part_and_workplace(day, part, workplace)

    def get_all_shifts_between_dates_for_given_worker(self, id, start_date, end_date):
        return self.repository.get_all_shifts_between_dates_for_given_worker(id, start_date, end_date)

    def get_shift_by_day_and_part(self, workplace_id, shift_date, shift_part):
        return self.repository.get_shift_by_day_and_part(workplace_id, shift_date, shift_part)

def convert_shift_for_client(shift: Shift, db, is_manager=True) -> dict:
    """
    Converts a shift to a dictionary format for client-side consumption.
    If the user is a manager, the dictionary will also include the workers assigned to the shift.

    Parameters:
        shift (Shift): The shift to convert.
        db (Session): SQLAlchemy Session for database interactions.
        is_manager (bool): A boolean indicating whether the user is a manager.

    Returns:
        dict: A dictionary representation of the shift.
    """
    shift_workers_controller = ShiftWorkersController(db)
    shifts_for_client = {
        "id": shift.id,
        "workPlaceID": shift.workPlaceID,
        # JSON can't handle date objects, so we convert them to strings
        'shiftDate': shift.shiftDate.isoformat() if shift.shiftDate else None,
        # JSON can't handle enum objects, so we take their values
        "shiftPart": shift.shiftPart.value
    }

    # If the user is a manager, we also include the workers assigned to the shift
    if is_manager:
        workers = shift_workers_controller.convert_shift_workers_by_shift_id_to_client(shift.id)
        shifts_for_client["workers"] = workers

    return shifts_for_client


def convert_shifts_for_client(shifts: list[Shift], db, is_manager=True) -> list[dict]:
    """
    Converts a list of shifts to a dictionary format for client-side consumption.

    Parameters:
        shifts (List[Shift]): The shifts to convert.
        db (Session): SQLAlchemy Session for database interactions.
        is_manager (bool): A boolean indicating whether the user is a manager.

    Returns:
        List[dict]: A list of dictionary representations of the shifts.
    """
    return [convert_shift_for_client(shift, db, is_manager) for shift in shifts]

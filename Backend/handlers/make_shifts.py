from datetime import datetime, timedelta
from enum import Enum
from Backend.config.constants import db
from Backend.db.controllers.shifts_controller import ShiftsController
from Backend.db.models import ShiftPart

class DayName(Enum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

def make_shifts(user_session):
    if user_session is None:
        print("User session not found.")
        return False

    if user_session.can_access_manager_page():
        shifts_controller = ShiftsController(db)
        current_date = datetime.now()
        next_sunday = current_date + timedelta(days=(6 - current_date.weekday() + 1) % 7)
        next_week_dates = [next_sunday + timedelta(days=i) for i in range(7)]
        shift_parts = [ShiftPart.Morning, ShiftPart.Noon, ShiftPart.Evening]
        days = [DayName.Sunday, DayName.Monday, DayName.Tuesday, DayName.Wednesday, DayName.Thursday, DayName.Friday,
                DayName.Saturday]
        for date in next_week_dates:
            for i in range(0, 3):
                shift = {"workPlaceID": user_session.get_id, "shiftDate": date.strftime("%Y-%m-%d"),
                         "shiftPart": shift_parts[i].value,
                         "shiftDay": days[datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d").weekday()].name}
                shifts_controller.create_entity(shift)

    else:
        print("User does not have access to manager-specific pages.")
        return False
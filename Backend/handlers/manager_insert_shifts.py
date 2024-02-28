from datetime import datetime, timedelta
from enum import Enum
from Backend.config.constants import db
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController
from Backend.db.controllers.shifts_controller import ShiftsController
from Backend.db.controllers.userRequests_controller import UserRequestsController
from Backend.db.controllers.users_controller import UsersController
from Backend.db.models import ShiftPart
from Backend.user_session import UserSession
from Backend.db.controllers.workPlaces_controller import WorkPlacesController


def handle_manager_insert_shifts(data, user_session: UserSession):
    if user_session.can_access_manager_page():
        work_places_controller = WorkPlacesController(db)
        shifts_controller = ShiftsController(db)
        shift_workers_controller = ShiftWorkersController(db)
        user_request_controller = UserRequestsController(db)
        users_controller = UsersController(db)
        employee_id = users_controller.get_user_id_by_username(data["username"])
        employee_request = user_request_controller.get_request_by_userid(employee_id)
        days = [DayName.Sunday, DayName.Monday, DayName.Tuesday, DayName.Wednesday, DayName.Thursday, DayName.Friday,
                DayName.Saturday]
        shift_parts = [ShiftPart.Morning, ShiftPart.Noon, ShiftPart.Evening]
        shifts = employee_request.split('_')
        for shift in shifts:
            shift_time, insert = shift.split('-')
            if insert == 't':
                part = 'm'
                if shift_time[1] == 'n':
                    part = shift_parts[1].value
                elif shift_time[1] == 'e':
                    part = shift_parts[2].value
                shift_id = shifts_controller.get_shift_id_by_day_and_part_and_workplace(
                    days[int(shift_time[0]) - 1].name, part, user_session.get_id)
                if shift_id is not None:
                    shift_worker = {'shiftID': shift_id, 'userID': employee_id}
                    shift_workers_controller.create_entity(shift_worker)

    else:
        print("User does not have access to manager-specific pages.")
        return False

def make_shifts(user_session: UserSession):
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


class DayName(Enum):  # I moved this class over here cuz it's not supposed to be in the models file
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

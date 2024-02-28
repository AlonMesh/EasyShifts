from datetime import datetime
from unittest import TestCase
from Backend.handlers.employee_shifts_request import handle_is_in_request_window
from Backend.config.constants import db
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.user_session import UserSession


class Test(TestCase):
    def setUp(self):
        """To execute the test, the database must be populated with the following data:
            - A manager user with id `e3e32ca5-2369-4a8a-975c-6676e360e666`.
            - A worker user with id `e3e32ca5-2369-4a8a-975c-6676e360e667`.
            - A shift board with the manager id as `MANAGER_ID`.
            - A workplace entity to connect the manager and worker users.
        """
        self.MANAGER_ID = "e3e32ca5-2369-4a8a-975c-6676e360e666"
        self.WORKER_ID = "e3e32ca5-2369-4a8a-975c-6676e360e667"
        self.shift_board_controller = ShiftBoardController(db)
        self.last_shift_board = self.shift_board_controller.get_last_shift_board(self.MANAGER_ID)
        self.TIME_NOW = datetime.now()
        self.user_session = UserSession(self.WORKER_ID, False)

    def test_handle_is_in_request_window(self):
        # First case, the current date is in the request window
        start_time = self.TIME_NOW.replace(day=self.TIME_NOW.day - 1)  # Yesterday
        end_time = self.TIME_NOW.replace(day=self.TIME_NOW.day + 1)  # Tomorrow
        self.last_shift_board.requests_window_start = start_time
        self.last_shift_board.requests_window_end = end_time

        result = handle_is_in_request_window(self.user_session)
        self.assertTrue(result)

        # Second case, the current date is not in the request window
        start_time = self.TIME_NOW.replace(day=self.TIME_NOW.day - 2)
        end_time = self.TIME_NOW.replace(day=self.TIME_NOW.day - 1)
        self.last_shift_board.requests_window_start = start_time
        self.last_shift_board.requests_window_end = end_time

        result = handle_is_in_request_window(self.user_session)
        self.assertFalse(result)


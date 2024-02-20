from datetime import timedelta
from unittest import TestCase
from Backend.db.models import next_sunday
from Backend.handlers.manager_schedule import handle_create_new_board
from Backend.user_session import UserSession


class Test(TestCase):
    def setUp(self):
        """To execute this test, the database must be populated with the following data:
            - A manager user with id `e3e32ca5-2369-4a8a-975c-6676e360e668`.
        """
        MANAGER_ID = "e3e32ca5-2369-4a8a-975c-6676e360e668"
        self.manager_id = MANAGER_ID
        self.user_session = UserSession(MANAGER_ID, True)
        self.next_sunday = next_sunday()

    def test_handle_create_new_board(self):
        # In case the manager wants to create his first board, it'll create a new board
        created_board = handle_create_new_board(self.user_session)

        # Assert the board was created and it's connected to the manager
        self.assertIsNotNone(created_board)
        self.assertEqual(created_board.workplaceID, self.manager_id)

        # Assert the board is created with the next Sunday as the start date
        self.assertEqual(created_board.weekStartDate, self.next_sunday)

        # In case the manager already has a board, it'll create a new board
        created_board = handle_create_new_board(self.user_session)

        # Assert the board was created and it's connected to the manager
        self.assertIsNotNone(created_board)
        self.assertEqual(created_board.workplaceID, self.manager_id)

        # Assert the board is created with the next-next Sunday as the start date
        next_next_sunday = self.next_sunday + timedelta(days=7)
        self.assertEqual(created_board.weekStartDate, next_next_sunday)


    def test_handle_get_board(self):
        self.fail()

    def test_handle_save_board(self):
        self.fail()

    def test_handle_reset_board(self):
        self.fail()

    def test_handle_publish_board(self):
        self.fail()

    def test_handle_unpublish_board(self):
        self.fail()

    def test_handle_get_board_content(self):
        self.fail()

    def test_schedule_worker_to_shift(self):
        self.fail()

    def test_unschedule_worker_from_shift(self):
        self.fail()

    def test_handle_schedules(self):
        self.fail()

    def test_watch_workers_requests(self):
        self.fail()

    def test_open_requests_windows(self):
        self.fail()

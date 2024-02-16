import datetime
from unittest import TestCase

from sqlalchemy import Date

from Backend.db.controllers.shiftBoard_controller import ShiftBoardController
from Backend.db.repositories.shiftBoard_repository import ShiftBoardRepository
from Backend.db.services.shiftBoard_service import ShiftBoardService
from Backend.main import initialize_database_and_session
from Backend.db.controllers.users_controller import UsersController  # To create a manager


class TestShiftBoardController(TestCase):
    def setUp(self):
        # Initialize the database and session
        self.db, _ = initialize_database_and_session()

        # Initialize the shift board controller
        shiftBoardRepository = ShiftBoardRepository(self.db)
        self.shiftBoardController = ShiftBoardController(shiftBoardRepository, ShiftBoardService(shiftBoardRepository))

    def test_create_shift_board(self):
        # First, create a manager
        manager_data = {
            "username": "test_manager",
            "password": "test_password",
            "isManager": True,
            "isActive": True,
            "isApproval": True,
            "name": "Test Manager"
        }
        users_controller = UsersController(self.db)
        manager = users_controller.create_entity(manager_data)

        # Create a shift board
        board_data = {
            "weekStartDate": "2021-10-04",
            "workplaceID": manager.id,
            "isPublished": False,
            "content": "bla-bla-bla",
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        # Check is not None
        board = self.shiftBoardController.create_shift_board(board_data)

        # Assert is not None
        self.assertTrue(board)

        # Assert is equal
        self.assertEqual(board.weekStartDate, datetime.date(2021, 10, 4))
        self.assertEqual(board.workplaceID, manager.id)
        self.assertEqual(board.isPublished, False)

        # Get the shift board
        board_get = self.shiftBoardController.get_shift_board(datetime.date(2021, 10, 4), manager.id)

        # Assert it equals to the created one
        self.assertEqual(board.workplaceID, board_get.workplaceID)

        # Update the shift board
        board_update_data = {
            "isPublished": True,
        }

        # Update the shift board
        board_update = self.shiftBoardController.update_shift_board(datetime.date(2021, 10, 4), manager.id,
                                                                    board_update_data)

        # Check it's updated
        self.assertEqual(board_update.isPublished, True)

        # Delete the shift board
        self.shiftBoardController.delete_shift_board(datetime.date(2021, 10, 4), manager.id)
        users_controller.delete_entity(manager.id)  # Delete the manager

        # Check it's deleted
        with self.assertRaises(Exception):
            self.shiftBoardController.get_shift_board(datetime.date(2021, 10, 4), manager.id)


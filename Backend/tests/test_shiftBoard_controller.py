import datetime
from unittest import TestCase
from Backend.db.controllers.shiftBoard_controller import ShiftBoardController, convert_shiftBoard_to_client
from Backend.db.models import ShiftPart
from Backend.main import initialize_database_and_session
from Backend.db.controllers.users_controller import UsersController  # To create a manager


class TestShiftBoardController(TestCase):
    def setUp(self):
        # Initialize the database and session
        self.db, _ = initialize_database_and_session()

        # Initialize the controllers
        self.shiftBoardController = ShiftBoardController(self.db)
        self.users_controller = UsersController(self.db)

        # Create a manager
        manager_data = {
            "username": "test_manager",
            "password": "test_password",
            "isManager": True,
            "isActive": True,
            "isApproval": True,
            "name": "Test Manager"
        }
        self.manager = self.users_controller.create_entity(manager_data)

        # Create a shift board
        board_data = {
            "workplaceID": self.manager.id,
            "isPublished": False,
            "content": {
                "Sunday": {
                    "shift1": ["worker1", "worker2"],
                    "shift2": ["worker3", "worker4"],
                    "shift3": ["worker5", "worker6"]
                },
            },
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        self.board = self.shiftBoardController.create_shift_board(board_data)

    def test_crud_shift_board(self):
        # Assert is not None
        self.assertTrue(self.board)

        # Assert is equal
        self.assertEqual(self.board.workplaceID, self.manager.id)
        self.assertEqual(self.board.isPublished, False)

        # Get the shift board
        NEXT_SUNDAY = datetime.date(2024, 2, 18)  # Modify this date to the next Sunday
        board_get = self.shiftBoardController.get_shift_board(NEXT_SUNDAY, self.manager.id)

        # Assert it equals to the created one
        self.assertEqual(self.board.workplaceID, board_get.workplaceID)

        # Update the shift board
        board_update_data = {
            "isPublished": True,
        }

        # Update the shift board
        board_update = self.shiftBoardController.update_shift_board(NEXT_SUNDAY, self.manager.id, board_update_data)

        # Check it's updated
        self.assertEqual(board_update.isPublished, True)

        # Delete the shift board and the manager
        self.shiftBoardController.delete_shift_board(NEXT_SUNDAY, self.manager.id)
        self.users_controller.delete_entity(self.manager.id)

        # Check it's deleted
        with self.assertRaises(Exception):
            self.shiftBoardController.get_shift_board(NEXT_SUNDAY, self.manager.id)

    def test_errors_of_create_shift(self):
        # Send invalid workplaceID
        board_data = {
            "workplaceID": "invalid_id",
            "isPublished": False,
            "content": {
                "Sunday": {
                    "shift1": ["worker1", "worker2"],
                    "shift2": ["worker3", "worker4"],
                    "shift3": ["worker5", "worker6"]
                },
            },
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        with self.assertRaises(ValueError):
            self.shiftBoardController.create_shift_board(board_data)

        # Send a used weekStartDate
        board_data = {
            "workplaceID": self.manager.id,
            "weekStartDate": self.board.weekStartDate,  # This date is already used
            "isPublished": False,
            "content": {
                "Sunday": {
                    "shift1": ["worker1", "worker2"],
                    "shift2": ["worker3", "worker4"],
                    "shift3": ["worker5", "worker6"]
                },
            },
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        with self.assertRaises(ValueError):
            self.shiftBoardController.create_shift_board(board_data)

        # Delete the manager and the shift board
        self.shiftBoardController.delete_shift_board(self.board.weekStartDate, self.manager.id)
        self.users_controller.delete_entity(self.manager.id)

    def test_work_with_several_boards(self):
        # A manager is created and a shift board is created
        # Create a future shift board
        board_data = {
            "weekStartDate": "2028-02-25",
            "workplaceID": self.manager.id,
            "isPublished": False,
            "content": {
                "Sunday": {
                    "shift1": ["worker1", "worker2"],
                    "shift2": ["worker3", "worker4"],
                    "shift3": ["worker5", "worker6"]
                },
            },
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        self.shiftBoardController.create_shift_board(board_data)

        # Create a past shift board
        board_data = {
            "weekStartDate": "2020-02-11",
            "workplaceID": self.manager.id,
            "isPublished": False,
            "content": {
                "Sunday": {
                    "shift1": ["worker1", "worker2"],
                    "shift2": ["worker3", "worker4"],
                    "shift3": ["worker5", "worker6"]
                },
            },
            "preferences": {
                "number_of_shifts_per_day": 3,
                "max_workers_per_shift": 5,
                "closed_days": ["Sunday", "Saturday"]
            }
        }

        self.shiftBoardController.create_shift_board(board_data)

        # Get all shift boards by workplace
        boards = self.shiftBoardController.get_all_shift_boards_by_workplace(self.manager.id)

        # Assert the length of the list
        self.assertEqual(len(boards), 3)

        # Get the last shift board
        last_board = self.shiftBoardController.get_last_shift_board(self.manager.id)

        # Assert it's the last one
        self.assertEqual(last_board.weekStartDate, datetime.date(2028, 2, 25))

        print(convert_shiftBoard_to_client(last_board))  # To see the output

        # Delete the manager and the shift boards
        self.shiftBoardController.delete_shift_board(self.board.weekStartDate, self.manager.id)
        self.shiftBoardController.delete_shift_board("2028-02-25", self.manager.id)
        self.shiftBoardController.delete_shift_board("2020-02-11", self.manager.id)
        self.users_controller.delete_entity(self.manager.id)

    def test_get_content_template_by_preferences(self):
        # Get the content template by preferences
        preferences = {
            "number_of_shifts_per_day": 2,
            "closed_days": ["Sunday", "Saturday"]
        }

        content_template = self.shiftBoardController.repository.get_content_template_by_preferences(preferences, self.manager.id)

        try:
            # Assert the content template
            self.assertEqual(content_template, {
                "Sunday": {
                    ShiftPart.Morning: "CLOSED",
                    ShiftPart.Noon: "CLOSED",
                },
                "Monday": {
                    ShiftPart.Morning: [],
                    ShiftPart.Noon: [],
                },
                "Tuesday": {
                    ShiftPart.Morning: [],
                    ShiftPart.Noon: [],
                },
                "Wednesday": {
                    ShiftPart.Morning: [],
                    ShiftPart.Noon: [],
                },
                "Thursday": {
                    ShiftPart.Morning: [],
                    ShiftPart.Noon: [],
                },
                "Friday": {
                    ShiftPart.Morning: [],
                    ShiftPart.Noon: [],
                },
                "Saturday": {
                    ShiftPart.Morning: "CLOSED",
                    ShiftPart.Noon: "CLOSED",
                }
            })
        finally:
            print(content_template)  # To see the output
            # Delete the manager and the shift board
            self.shiftBoardController.delete_shift_board(self.board.weekStartDate, self.manager.id)
            self.users_controller.delete_entity(self.manager.id)


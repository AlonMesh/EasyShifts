from unittest import TestCase
from datetime import datetime
from Backend.main import initialize_database_and_session
from Backend.db.controllers import userRequests_controller, workPlaces_controller, shiftWorkers_controller, \
    users_controller, shifts_controller


# If importing `initialize_database_and_session` and `create_tables` don't work, put them here:

# End.

class TestCheckSetup(TestCase):
    """Test case for checking setup and entity creation."""
    def setUp(self):
        # Initialize a test database and session
        self.db, _ = initialize_database_and_session()

    def test_user_creation(self):
        # Check User creation
        user_data = {
            "username": "zz",
            "password": "8",
            "isManager": 0,
            "isActive": 1,
            "name": "test user"
        }

        # Initialize Controller
        controller = users_controller.UsersController(self.db)

        created_user = controller.create_entity(entity_data=user_data)
        self.assertIsNotNone(created_user)

    def test_workplace_creation(self):
        # Check WorkPlace creation
        workplace_data = {
            "id": 23,
            "workPlaceID": 1
        }

        # Initialize Controller
        controller = workPlaces_controller.WorkPlacesController(self.db)

        created_workplace = controller.create_entity(entity_data=workplace_data)
        self.assertIsNotNone(created_workplace)

    def test_user_request_creation(self):
        # Check UserRequest creation
        user_request_data = {
            "id": 1,
            "modifyAt": datetime(2024, 1, 30, 12, 0, 0),
            "requests": "Any request..."
        }
        # Initialize Controller
        controller = userRequests_controller.UserRequestsController(self.db)

        created_user_request = controller.create_entity(entity_data=user_request_data)
        self.assertIsNotNone(created_user_request)

    def test_shift_creation(self):
        # Check Shift creation
        shift_data = {
            "workPlaceID": 1,
            "shiftDate": datetime(2024, 1, 30, 8, 0, 0),
            "shiftPart": "Morning"
        }
        # Initialize Controller
        controller = shifts_controller.ShiftsController(self.db)

        created_shift = controller.create_entity(entity_data=shift_data)
        self.assertIsNotNone(created_shift)

    def test_z_shift_worker_creation(self):
        # Check ShiftWorker creation
        shift_worker_data = {
            "shiftID": 1,
            "userID": 1
        }
        # Initialize Controller
        controller = shiftWorkers_controller.ShiftWorkersController(self.db)

        created_shift_workers = controller.create_entity(entity_data=shift_worker_data)
        self.assertIsNotNone(created_shift_workers)

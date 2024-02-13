from unittest import TestCase
from datetime import datetime
from Backend.main import initialize_database_and_session
from Backend.db.controllers import userRequests_controller, workPlaces_controller, shiftWorkers_controller, \
    users_controller, shifts_controller
from Backend.db.models import ShiftPart


# If importing `initialize_database_and_session` and `create_tables` don't work, put them here:

# End.

class TestCheckSetup(TestCase):
    """Test case for checking setup and entity creation."""
    def setUp(self):
        # Initialize a test database and session
        self.db, _ = initialize_database_and_session()

    def test_check_setup(self, keep_entities=False):
        """
        Test the setup and entity creation. Args: keep_entities: If True, the entities will not be removed after the
        test. It is recommended to change it to True in the first time to see how the entities are looking like.
        Then, delete all tables and recreate it when it is False.
        """
        # Check User creation
        user_data = {
            "username": "test_worker",
            "password": "pass",
            "isManager": 0,
            "isActive": 1,
            "name": "test user"
        }

        # Initialize Controller
        user_controller = users_controller.UsersController(self.db)

        created_user = user_controller.create_entity(entity_data=user_data)
        self.assertIsNotNone(created_user)

        manager_data = {
            "username": "test_Manager",
            "password": "pass",
            "isManager": 1,
            "isActive": 1,
            "name": "Manager Company"
        }
        created_manager = user_controller.create_entity(entity_data=manager_data)  # Assume it works well

        # Check WorkPlace creation
        workplace_data = {
            "id": created_user.id,
            "workPlaceID": created_manager.id
        }

        # Initialize Controller
        workplace_controller = workPlaces_controller.WorkPlacesController(self.db)

        created_workplace = workplace_controller.create_entity(entity_data=workplace_data)
        self.assertIsNotNone(created_workplace)

        # Check UserRequest creation
        user_request_data = {
            "id": created_user.id,
            "modifyAt": datetime(2024, 1, 30, 12, 0, 0),
            "requests": "Any request..."
        }
        # Initialize Controller
        user_request_controller = userRequests_controller.UserRequestsController(self.db)

        created_user_request = user_request_controller.create_entity(entity_data=user_request_data)
        self.assertIsNotNone(created_user_request)

        # Check Shift creation
        shift_data = {
            "workPlaceID": created_manager.id,
            "shiftDate": datetime(2024, 1, 30, ),
            "shiftPart": ShiftPart.Morning.value
        }
        # Initialize Controller
        shift_controller = shifts_controller.ShiftsController(self.db)

        created_shift = shift_controller.create_entity(entity_data=shift_data)
        self.assertIsNotNone(created_shift)

        # Check ShiftWorker creation
        shift_worker_data = {
            "shiftID": created_shift.id,
            "userID": created_user.id
        }
        # Initialize Controller
        shift_workers_controller = shiftWorkers_controller.ShiftWorkersController(self.db)

        created_shift_workers = shift_workers_controller.create_entity(entity_data=shift_worker_data)
        self.assertIsNotNone(created_shift_workers)

        if not keep_entities:
            # Remove entities
            shift_workers_controller.delete_entity_shift_worker(created_shift_workers.shiftID, created_shift_workers.userID)
            workplace_controller.delete_entity(created_workplace.id)
            user_request_controller.delete_entity(created_user_request.id)
            shift_controller.delete_entity(created_shift.id)
            user_controller.delete_entity(created_user.id)
            user_controller.delete_entity(created_manager.id)

from unittest import TestCase
from Backend.main import initialize_database_and_session
from Backend.db.repositories.shiftWorkers_repository import ShiftWorkersRepository
from Backend.db.repositories.users_repository import UsersRepository
from Backend.db.repositories.shifts_repository import ShiftsRepository


class TestShiftWorkersRepository(TestCase):
    def setUp(self):
        # Initialize db
        db, _ = initialize_database_and_session()

        # Instantiate repository
        self.shift_workers_repository = ShiftWorkersRepository(db)

    def test_get_worker_shifts_by_worker_id(self):
        # Generate a temporary user to be used as a worker
        user_data = {"username": "test_user_shift", "password": "test_pass", "isManager": 0, "isActive": 1, "name": "test user"}
        user_repository = UsersRepository(self.shift_workers_repository.db)
        created_user = user_repository.create_entity(user_data)

        # Generate 3 shifts to be used as the worker's shifts
        shift_data_1 = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Morning"}
        shift_data_2 = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Afternoon"}
        shift_data_3 = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Night"}

        shift_repository = ShiftsRepository(self.shift_workers_repository.db)
        created_shift_1 = shift_repository.create_entity(shift_data_1)
        created_shift_2 = shift_repository.create_entity(shift_data_2)
        created_shift_3 = shift_repository.create_entity(shift_data_3)

        # Add an entity to the database
        data = {"shiftID": created_shift_1.id, "userID": created_user.id}
        created_shift_worker_1 = self.shift_workers_repository.create_entity(data)
        data = {"shiftID": created_shift_2.id, "userID": created_user.id}
        created_shift_worker_2 = self.shift_workers_repository.create_entity(data)
        data = {"shiftID": created_shift_3.id, "userID": created_user.id}
        created_shift_worker_3 = self.shift_workers_repository.create_entity(data)

        try:
            # Check that the worker has 3 shifts
            self.assertEqual(len(self.shift_workers_repository.get_worker_shifts_by_worker_id(created_user.id)), 3)
        # If there's any error, delete the entities from the database
        except:
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_1.shiftID, created_shift_worker_1.userID)
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_2.shiftID, created_shift_worker_2.userID)
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_3.shiftID, created_shift_worker_3.userID)
            user_repository.delete_entity(created_user.id)
            shift_repository.delete_entity(created_shift_1.id)
            shift_repository.delete_entity(created_shift_2.id)
            shift_repository.delete_entity(created_shift_3.id)
            self.fail()

        # Delete the entities from the database
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_1.shiftID, created_shift_worker_1.userID)
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_2.shiftID, created_shift_worker_2.userID)
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_3.shiftID, created_shift_worker_3.userID)
        user_repository.delete_entity(created_user.id)
        shift_repository.delete_entity(created_shift_1.id)
        shift_repository.delete_entity(created_shift_2.id)
        shift_repository.delete_entity(created_shift_3.id)

    def test_get_shift_workers_by_shift_id(self):
        # Generate a temporary users to be used as workers
        user_data_1 = {"username": "test_user_shift_1", "password": "test_pass", "isManager": 0, "isActive": 1, "name": "test user"}
        user_data_2 = {"username": "test_user_shift_2", "password": "test_pass", "isManager": 0, "isActive": 1, "name": "test user"}
        user_repository = UsersRepository(self.shift_workers_repository.db)
        created_user_1 = user_repository.create_entity(user_data_1)
        created_user_2 = user_repository.create_entity(user_data_2)

        # Generate a shift to be used as the workers' shift
        shift_data = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Morning"}
        shift_repository = ShiftsRepository(self.shift_workers_repository.db)
        created_shift = shift_repository.create_entity(shift_data)

        # Add entities to the database
        data_1 = {"shiftID": created_shift.id, "userID": created_user_1.id}
        created_shift_worker_1 = self.shift_workers_repository.create_entity(data_1)
        data_2 = {"shiftID": created_shift.id, "userID": created_user_2.id}
        created_shift_worker_2 = self.shift_workers_repository.create_entity(data_2)

        try:
            # Check that the shift has 2 workers
            self.assertEqual(len(self.shift_workers_repository.get_shift_workers_by_shift_id(created_shift.id)), 2)
        # If there's any error, delete the entities from the database
        except:
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_1.shiftID, created_shift_worker_1.userID)
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_2.shiftID, created_shift_worker_2.userID)
            user_repository.delete_entity(created_user_1.id)
            user_repository.delete_entity(created_user_2.id)
            shift_repository.delete_entity(created_shift.id)
            self.fail()

        # Delete the entities from the database
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_1.shiftID, created_shift_worker_1.userID)
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker_2.shiftID, created_shift_worker_2.userID)
        user_repository.delete_entity(created_user_1.id)
        user_repository.delete_entity(created_user_2.id)
        shift_repository.delete_entity(created_shift.id)

    def test_is_shift_assigned_to_worker(self):
        # Generate a temporary user to be used as a worker
        user_data = {"username": "test_user_shift", "password": "test_pass", "isManager": 0, "isActive": 1, "name": "test user"}
        user_repository = UsersRepository(self.shift_workers_repository.db)
        created_user = user_repository.create_entity(user_data)

        # Generate a shift to be used as the worker's shift
        true_shift_data = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Morning"}
        shift_repository = ShiftsRepository(self.shift_workers_repository.db)
        created_true_shift = shift_repository.create_entity(true_shift_data)

        # Generate a shift to be used as a different shift
        false_shift_data = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": "Afternoon"}
        created_false_shift = shift_repository.create_entity(false_shift_data)

        # Add an entity to the database
        data = {"shiftID": created_true_shift.id, "userID": created_user.id}
        created_shift_worker = self.shift_workers_repository.create_entity(data)

        try:
            # Check that the shift is assigned to the worker
            self.assertTrue(self.shift_workers_repository.is_shift_assigned_to_worker(created_true_shift.id, created_user.id))

            # Check that the shift is not assigned to the worker
            self.assertFalse(self.shift_workers_repository.is_shift_assigned_to_worker(created_false_shift.id, created_user.id))
        # If there's any error, delete the entities from the database
        except:
            self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker.shiftID, created_shift_worker.userID)
            user_repository.delete_entity(created_user.id)
            shift_repository.delete_entity(created_true_shift.id)
            shift_repository.delete_entity(created_false_shift.id)
            self.fail()

        # Delete the entities from the database
        self.shift_workers_repository.delete_entity_shift_worker(created_shift_worker.shiftID, created_shift_worker.userID)
        user_repository.delete_entity(created_user.id)
        shift_repository.delete_entity(created_true_shift.id)
        shift_repository.delete_entity(created_false_shift.id)

    def test_is_shift_assigned_to_worker_user_not_found(self):
        # Call the function with an invalid user_id
        with self.assertRaises(Exception):
            self.shift_workers_repository.is_shift_assigned_to_worker(1, -1)

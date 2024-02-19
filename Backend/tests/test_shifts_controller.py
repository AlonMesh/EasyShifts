import datetime
from unittest import TestCase
from sqlalchemy.exc import NoResultFound
from Backend.db.controllers.shifts_controller import ShiftsController, convert_shift_for_client
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.shiftWorkers_controller import ShiftWorkersController
from Backend.main import initialize_database_and_session
from Backend.db.models import ShiftPart


class TestShiftsController(TestCase):
    def setUp(self):
        # Initialize db
        self.db, _ = initialize_database_and_session()

        # Instantiate controller
        self.shift_controller = ShiftsController(self.db)

    def test_get_shift_date_by_shift_id_exists(self):
        # Add an entity to the database
        shift_data = {
            "id": 999,
            "workPlaceID": 999,
            "shiftDate": "2022-12-12",
            "shiftPart": ShiftPart.Morning
        }
        created_shift = self.shift_controller.create_entity(shift_data)

        # Get the entity from the database
        retrieved_shift = self.shift_controller.get_entity(created_shift.id)

        try:
            # Assert that the retrieved entity matches the added entity
            self.assertEqual(created_shift.id, retrieved_shift.id)

            # Assert that the shift date is correct
            expected_date = datetime.date(2022, 12, 12)
            self.assertEqual(self.shift_controller.get_shift_date_by_shift_id(created_shift.id), expected_date)
        except:
            # Delete the entity from the database
            self.shift_controller.delete_entity(created_shift.id)
            self.fail()

        # Delete the entity from the database
        self.shift_controller.delete_entity(created_shift.id)

    def test_get_shift_date_by_shift_id_not_found(self):
        # Call the function with an invalid shift_id
        with self.assertRaises(NoResultFound):
            self.shift_controller.get_shift_date_by_shift_id("-1")

    def test_get_all_shifts_since_date(self):
        # Check the amount of shifts in the database
        current_shifts_count = len(self.shift_controller.get_all_entities())

        # Add an entity to the database
        shift_data_1 = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": ShiftPart.Morning}
        shift_data_2 = {"workPlaceID": 1, "shiftDate": "2022-12-11", "shiftPart": ShiftPart.Noon}
        shift_data_3 = {"workPlaceID": 1, "shiftDate": "2022-12-10", "shiftPart": ShiftPart.Evening}

        # Create the entities
        created_shift_1 = self.shift_controller.create_entity(shift_data_1)
        created_shift_2 = self.shift_controller.create_entity(shift_data_2)
        created_shift_3 = self.shift_controller.create_entity(shift_data_3)

        # Get all shifts since a given date
        shifts = self.shift_controller.get_all_shifts_of_worker_since_date(datetime.date(2022, 12, 9))
        shifts_ids = [shift.id for shift in shifts]

        try:
            # Assert that the retrieved shifts are correct
            self.assertEqual(len(shifts) - current_shifts_count, 3)
            self.assertIn(created_shift_1.id, shifts_ids)
            self.assertIn(created_shift_2.id, shifts_ids)
            self.assertIn(created_shift_3.id, shifts_ids)
        except:
            # Delete the entities from the database
            self.shift_controller.delete_entity(created_shift_1.id)
            self.shift_controller.delete_entity(created_shift_2.id)
            self.shift_controller.delete_entity(created_shift_3.id)
            self.fail()

        # Delete the entities from the database
        self.shift_controller.delete_entity(created_shift_1.id)
        self.shift_controller.delete_entity(created_shift_2.id)
        self.shift_controller.delete_entity(created_shift_3.id)

    def test_get_all_shifts_since_date_for_given_worker(self):
        # Add an entity to the database
        shift_data_1 = {"workPlaceID": 1, "shiftDate": "2022-12-12", "shiftPart": ShiftPart.Morning}
        shift_data_2 = {"workPlaceID": 1, "shiftDate": "2022-12-11", "shiftPart": ShiftPart.Noon}
        shift_data_3 = {"workPlaceID": 1, "shiftDate": "2022-12-10", "shiftPart": ShiftPart.Evening}

        # Create the entities
        created_shift_1 = self.shift_controller.create_entity(shift_data_1)
        created_shift_2 = self.shift_controller.create_entity(shift_data_2)
        created_shift_3 = self.shift_controller.create_entity(shift_data_3)

        # Create a worker
        worker_data = {'username': "test_user_3", 'password': "1234", 'isManager': 0, 'isActive': 1, 'name': "name"}
        user_controller = UsersController(self.db)  # Instantiate the user controller
        worker = user_controller.create_entity(worker_data)

        # Connect the worker to the shifts
        shift_workers_controller = ShiftWorkersController(self.db)
        shift_workers_controller.create_entity({'shiftID': created_shift_1.id, 'userID': worker.id})
        shift_workers_controller.create_entity({'shiftID': created_shift_2.id, 'userID': worker.id})
        shift_workers_controller.create_entity({'shiftID': created_shift_3.id, 'userID': worker.id})

        try:
            # Get all shifts since a given date for a given worker
            shifts = self.shift_controller.get_all_shifts_since_date_for_given_worker(datetime.date(2022, 12, 11),
                                                                                      worker.id)
            shifts_ids = [shift.id for shift in shifts]

            # Assert that the retrieved shifts are correct
            self.assertEqual(len(shifts), 2)
            self.assertIn(created_shift_1.id, shifts_ids)
            self.assertIn(created_shift_2.id, shifts_ids)
            self.assertNotIn(created_shift_3.id, shifts_ids)
        except:
            # Delete the entities from the database
            shift_workers_controller.delete_entity_shift_worker(created_shift_1.id, worker.id)
            shift_workers_controller.delete_entity_shift_worker(created_shift_2.id, worker.id)
            shift_workers_controller.delete_entity_shift_worker(created_shift_3.id, worker.id)
            self.shift_controller.delete_entity(created_shift_1.id)
            self.shift_controller.delete_entity(created_shift_2.id)
            self.shift_controller.delete_entity(created_shift_3.id)
            user_controller.delete_entity(worker.id)
            self.fail()

        # Delete the entities from the database
        shift_workers_controller.delete_entity_shift_worker(created_shift_1.id, worker.id)
        shift_workers_controller.delete_entity_shift_worker(created_shift_2.id, worker.id)
        shift_workers_controller.delete_entity_shift_worker(created_shift_3.id, worker.id)
        self.shift_controller.delete_entity(created_shift_1.id)
        self.shift_controller.delete_entity(created_shift_2.id)
        self.shift_controller.delete_entity(created_shift_3.id)
        user_controller.delete_entity(worker.id)

    def test_get_all_shifts_since_date_for_given_workplace(self):
        # Get current shifts count
        current_shifts_count = len(self.shift_controller.get_all_entities())

        # Add an entity to the database
        shift_data_1 = {"workPlaceID": "999", "shiftDate": "2022-12-12", "shiftPart": ShiftPart.Morning}
        shift_data_2 = {"workPlaceID": "999", "shiftDate": "2022-12-11", "shiftPart": ShiftPart.Noon}
        shift_data_3 = {"workPlaceID": "999", "shiftDate": "2022-12-10", "shiftPart": ShiftPart.Evening}

        # Create the entities
        created_shift_1 = self.shift_controller.create_entity(shift_data_1)
        created_shift_2 = self.shift_controller.create_entity(shift_data_2)
        created_shift_3 = self.shift_controller.create_entity(shift_data_3)

        try:
            # Get all shifts since a given date for a given workplace
            given_date = datetime.date(2022, 12, 11)
            workplace_id = "999"
            shifts = self.shift_controller.get_all_shifts_since_date_for_given_workplace(given_date, workplace_id)
            shifts_ids = [shift.id for shift in shifts]

            # Assert that the retrieved shifts are correct
            self.assertEqual(len(shifts) - current_shifts_count, 2)
            self.assertIn(created_shift_1.id, shifts_ids)
            self.assertIn(created_shift_2.id, shifts_ids)
            self.assertNotIn(created_shift_3.id, shifts_ids)
        except:
            # Delete the entities from the database
            self.shift_controller.delete_entity(created_shift_1.id)
            self.shift_controller.delete_entity(created_shift_2.id)
            self.shift_controller.delete_entity(created_shift_3.id)
            self.fail()

        # Delete the entities from the database
        self.shift_controller.delete_entity(created_shift_1.id)
        self.shift_controller.delete_entity(created_shift_2.id)
        self.shift_controller.delete_entity(created_shift_3.id)

    def test_get_future_shifts_for_workplace(self):
        # Get current shifts count
        current_shifts_count = len(self.shift_controller.get_all_entities())

        # Add an entity to the database
        shift_data_1 = {"workPlaceID": "999", "shiftDate": "2025-12-12", "shiftPart": ShiftPart.Morning}
        shift_data_2 = {"workPlaceID": "999", "shiftDate": "2022-12-11", "shiftPart": ShiftPart.Noon}
        shift_data_3 = {"workPlaceID": "999", "shiftDate": "2022-12-10", "shiftPart": ShiftPart.Evening}

        # Create the entities
        created_shift_1 = self.shift_controller.create_entity(shift_data_1)
        created_shift_2 = self.shift_controller.create_entity(shift_data_2)
        created_shift_3 = self.shift_controller.create_entity(shift_data_3)

        try:
            # Get all future shifts for a given workplace
            shifts = self.shift_controller.get_future_shifts_for_workplace("999")
            shifts_ids = [shift.id for shift in shifts]

            # Assert that the retrieved shifts are correct
            self.assertEqual(len(shifts) - current_shifts_count, 1)
            self.assertIn(created_shift_1.id, shifts_ids)
            self.assertNotIn(created_shift_2.id, shifts_ids)
            self.assertNotIn(created_shift_3.id, shifts_ids)
        except:
            # Delete the entities from the database
            self.shift_controller.delete_entity(created_shift_1.id)
            self.shift_controller.delete_entity(created_shift_2.id)
            self.shift_controller.delete_entity(created_shift_3.id)
            self.fail()

        # Delete the entities from the database
        self.shift_controller.delete_entity(created_shift_1.id)
        self.shift_controller.delete_entity(created_shift_2.id)
        self.shift_controller.delete_entity(created_shift_3.id)

    def test_convert_shift_for_client(self):
        # Add an entity to the database
        shift_data = {"workPlaceID": "999", "shiftDate": "2025-12-12", "shiftPart": ShiftPart.Morning}

        # Create the entity
        created_shift = self.shift_controller.create_entity(shift_data)

        # Convert the shift for client
        shift_for_client = convert_shift_for_client(created_shift, self.db)

        # Assert that the converted shift is correct
        self.assertEqual(shift_for_client, {
            "id": created_shift.id,
            "workPlaceID": created_shift.workPlaceID,
            "shiftDate": created_shift.shiftDate.isoformat(),
            "shiftPart": created_shift.shiftPart,
            "workers": []
        })

        print(shift_for_client)  # To see the output clearly

        # Delete the entity from the database
        self.shift_controller.delete_entity(created_shift.id)

import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from sqlalchemy.exc import NoResultFound

from Backend.main import initialize_database_and_session
from Backend.db.repositories.shifts_repository import ShiftsRepository


class TestShiftsRepository(TestCase):
    def setUp(self):
        # Initialize db
        db, _ = initialize_database_and_session()

        # Instantiate repository
        self.shift_repository = ShiftsRepository(db)

    def test_get_shift_date_by_shift_id_exists(self):
        # Add an entity to the database
        shift_data = {
            "id": 999,
            "workPlaceID": 999,
            "shiftDate": "2022-12-12",
            "shiftPart": "Morning"
        }
        created_shift = self.shift_repository.create_entity(shift_data)

        # Get the entity from the database
        retrieved_shift = self.shift_repository.get_entity(created_shift.id)

        # Assert that the retrieved entity matches the added entity
        self.assertEqual(created_shift, retrieved_shift)

        # Assert that the shift date is correct
        expected_date = datetime.datetime(2022, 12, 12)
        self.assertEqual(self.shift_repository.get_shift_date_by_shift_id(created_shift.id), expected_date)

        # Delete the entity from the database
        self.shift_repository.delete_entity(created_shift.id)

    def test_get_shift_date_by_shift_id_not_found(self):
        # Call the function with an invalid shift_id
        with self.assertRaises(NoResultFound):
            self.shift_repository.get_shift_date_by_shift_id(-1)

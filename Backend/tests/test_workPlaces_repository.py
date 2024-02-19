from unittest import TestCase
from Backend.db.controllers.users_controller import UsersController
from Backend.db.controllers.workPlaces_controller import WorkPlacesController
from Backend.main import initialize_database_and_session


class TestWorkPlacesRepository(TestCase):
    def setUp(self):
        db, _ = initialize_database_and_session()
        self.db = db
        self.controller = WorkPlacesController(self.db)

    def test_get_workplace_and_workplace_name_by_worker_id(self):
        workplace_data = {'username': 'Test_Place', 'password': 'pass', 'isManager': 1, 'isActive': 1, 'name': 'Test Place'}
        worker_data = {'username': 'Test_Worker', 'password': 'pass', 'isManager': 0, 'isActive': 1, 'name': 'Test Worker'}

        # Initialize the users controller, passing the database session
        users_controller = UsersController(self.db)

        # Create a workplace
        workplace = users_controller.create_entity(workplace_data)
        worker = users_controller.create_entity(worker_data)

        # Check if the workplace & worker exist
        self.assertIsNotNone(workplace)
        self.assertIsNotNone(worker)

        # Pass a Workplace entity to the database
        workplace = self.controller.create_entity({'id': worker.id, 'workPlaceID': workplace.id})

        # Check if the workplace exists
        self.assertIsNotNone(workplace)

        # Assert that the workplace name is as expected
        self.assertEqual("Test Place", self.controller.get_workplace_name_by_worker_id(worker.id))

        # Assert that the workplace is as expected
        self.assertEqual(workplace, self.controller.get_workplace_by_worker_id(worker.id))

        # Delete the workplace and worker
        workplace_id = workplace.id
        self.controller.delete_entity(workplace_id)
        # users_controller.delete_entity(worker.id)
        # users_controller.delete_entity(workplace_id)

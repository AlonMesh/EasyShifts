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

    def test_get_all_workers_by_workplace_id(self):
        workplace_data = {'username': 'Test_Place', 'password': 'pass', 'isManager': 1, 'isActive': 1, 'name': 'Place'}
        worker_data_1 = {'username': 'Yu', 'password': 'pass', 'isManager': 0, 'isActive': 1, 'name': 'Yu'}
        worker_data_2 = {'username': 'Gi', 'password': 'pass', 'isManager': 0, 'isActive': 1, 'name': 'Gi'}
        worker_data_3 = {'username': 'Oh', 'password': 'pass', 'isManager': 0, 'isActive': 1, 'name': 'Oh'}

        # Initialize the users controller, passing the database session
        users_controller = UsersController(self.db)

        # Create a workplace
        workplace = users_controller.create_entity(workplace_data)

        # Create workers
        worker1 = users_controller.create_entity(worker_data_1)
        worker2 = users_controller.create_entity(worker_data_2)
        worker3 = users_controller.create_entity(worker_data_3)

        # Create a workplaces entities to the workers
        workplace_1 = self.controller.create_entity({"id": worker1.id, "workPlaceID": workplace.id})
        workplace_2 = self.controller.create_entity({"id": worker2.id, "workPlaceID": workplace.id})
        workplace_3 = self.controller.create_entity({"id": worker3.id, "workPlaceID": workplace.id})

        try:
            # Check if the workplace & worker exist
            self.assertIsNotNone(workplace)
            self.assertIsNotNone(workplace_1)
            self.assertIsNotNone(workplace_2)
            self.assertIsNotNone(workplace_3)

            # Pass a Workplace
            workers_list = self.controller.get_all_workers_by_workplace_id(workplace.id)

            # Get the id of the workers
            workers_list = [worker.id for worker in workers_list]

            self.assertEqual(len(workers_list), 3)
            self.assertIn(workplace_1.id, workers_list)
            self.assertIn(workplace_2.id, workers_list)
            self.assertIn(workplace_3.id, workers_list)
        finally:
            # Delete the workplace entities
            self.controller.delete_entity(workplace_1.id)
            self.controller.delete_entity(workplace_2.id)
            self.controller.delete_entity(workplace_3.id)
            # Delete the workers and the manager
            users_controller.delete_entity(worker1.id)
            users_controller.delete_entity(worker2.id)
            users_controller.delete_entity(worker3.id)
            users_controller.delete_entity(workplace.id)

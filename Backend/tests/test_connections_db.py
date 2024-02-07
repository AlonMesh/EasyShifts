from unittest import TestCase
from Backend.db.repositories.users_repository import UsersRepository
from Backend.db.services.users_service import UsersService
from Backend.db.controllers.users_controller import UsersController
from Backend.main import initialize_database_and_session
from Backend.db.models import User


class TestConnectionsDB(TestCase):
    """Test class for checking connections between repository, service, and controller."""

    def setUp(self):
        # Initialize db
        self.db, _ = initialize_database_and_session()

        # Instantiate repository, service, and controller
        self.repository = UsersRepository(self.db)
        self.service = UsersService(self.repository)
        self.controller = UsersController(self.db)

    def test_repo_works(self):
        # Check if the entity_type of the repository is User
        self.assertEqual(self.repository.entity_type, User)

    def test_service_works(self):
        # Check if the entity_type of the service repository is User
        self.assertEqual(self.service.repository.entity_type, User)

    def test_service_does_CURD(self):
        user_data = {
            "username": "ser_test_user",
            "password": "ser_test_pass",
            "isManager": 0,
            "isActive": 1,
            "name": "con test user"
        }

        # Create
        created_user = self.service.repository.create_entity(user_data)
        self.assertIsNotNone(created_user)

        # Update
        updated_data = {'username': 'con_test_user', 'isActive': 0}
        updated_user = self.service.repository.update_entity(created_user.id, updated_data)
        self.assertIsNotNone(updated_user)

        # Delete
        self.service.repository.delete_entity(updated_user.id)

    def test_controller_works(self):
        # Check if the entity_type of the controller repository & service is User
        self.assertEqual(self.controller.repository.entity_type, User)
        self.assertEqual(self.controller.service.repository.entity_type, User)

    def test_controller_does_CURD(self):
        user_data = {
            "username": "con_test_user",
            "password": "con_test_pass",
            "isManager": 0,
            "isActive": 1,
            "name": "con test user"
        }

        # Create
        created_user = self.controller.create_entity(user_data)
        self.assertIsNotNone(created_user)

        # Update
        updated_data = {'username': 'con_test_user', 'isActive': 0}
        updated_user = self.controller.update_entity(created_user.id, updated_data)
        self.assertIsNotNone(updated_user)

        # Delete
        self.controller.delete_entity(updated_user.id)

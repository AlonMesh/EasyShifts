from unittest import TestCase
from Backend.db.controllers.users_controller import UsersController
from Backend.db.models import User
from Backend.db.repositories.users_repository import UsersRepository
from Backend.main import initialize_database_and_session
import string
import random


def generate_random_user_name(length: int = 12) -> str:
    """Generate a random username with the specified length."""
    characters = string.ascii_letters + string.digits
    random_username = ''.join(random.choice(characters) for i in range(length))
    return random_username


def arrange_user_data(password='test_password', is_manager=0, is_active=1, name='Test User'):
    """Arrange and return user data for testing."""
    return {'username': generate_random_user_name(), 'password': password, 'isManager': is_manager,
            'isActive': is_active, 'name': name}


class TestUsersRepository(TestCase):
    """Test case for UsersRepository class."""

    def setUp(self):
        """Set up the test environment."""
        # Initialize a test database
        db, session = initialize_database_and_session()
        self.db = db
        self.session = session
        self.users_repo = UsersRepository(self.db)
        self.users_controller = UsersController(self.db)

    def delete_user(self, user):
        """Delete the user from the database."""
        self.users_repo.delete_entity(user.id)

    def test_create_user(self):
        """Test creating a user and verifying its properties."""
        # Arrange
        user_data = arrange_user_data()

        # Act
        created_user = self.users_repo.create_entity(user_data)

        # Assert
        self.assertIsInstance(created_user, User)
        self.assertEqual(created_user.username, user_data['username'])

        self.delete_user(created_user)

    def test_get_user(self):
        """Test retrieving a user and verifying its correctness."""
        # Arrange
        user_data = arrange_user_data()
        created_user = self.users_repo.create_entity(user_data)

        # Act
        retrieved_user = self.users_repo.get_entity(created_user.id)

        # Assert
        self.assertEqual(retrieved_user.id, created_user.id)

        self.delete_user(created_user)

    def test_get_all_users(self):
        """Test retrieving all users and verifying the expected count and presence of created users."""
        all_users_before = self.users_repo.get_all_entities()

        # Arrange
        user_data_1 = arrange_user_data()
        user_data_2 = arrange_user_data()

        # Act
        user_1 = self.users_repo.create_entity(user_data_1)
        user_2 = self.users_repo.create_entity(user_data_2)

        all_users_after = self.users_repo.get_all_entities()
        ids = [user.id for user in all_users_after]

        # Assert
        self.assertEqual(len(all_users_after) - len(all_users_before), 2)
        self.assertIn(user_1.id, ids)
        self.assertIn(user_2.id, ids)

        self.delete_user(user_1)
        self.delete_user(user_2)

    def test_update_user(self):
        """Test updating a user and verifying the changes."""
        user_data = arrange_user_data()
        created_user = self.users_repo.create_entity(user_data)

        updated_data = {'username': 'updated_user', 'isActive': 0}

        # Act
        updated_user = self.users_repo.update_entity(created_user.id, updated_data)

        # Assert
        self.assertEqual(updated_user.username, updated_data['username'])
        self.assertEqual(updated_user.isActive, updated_data['isActive'])

        self.delete_user(updated_user)

    def test_delete_user(self):
        """Test deleting a user and ensuring it no longer exists in the database."""
        # Arrange
        user_data = arrange_user_data()
        created_user = self.users_repo.create_entity(user_data)
        created_user_id_keeper = created_user.id

        # Act
        self.users_repo.delete_entity(created_user.id)

        # Assert that the user no longer exists
        try:
            self.users_repo.get_entity(created_user_id_keeper)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_get_username_by_id(self):
        """Test retrieving a username by user ID."""
        # Arrange
        user_data = arrange_user_data()
        created_user = self.users_repo.create_entity(user_data)

        # Act
        retrieved_username = self.users_controller.get_username_by_id(created_user.id)

        # Assert
        self.assertEqual(retrieved_username, created_user.username)

        self.delete_user(created_user)

    def test_get_name_by_id(self):
        """Test retrieving a name by user ID."""
        # Arrange
        user_data = arrange_user_data()
        created_user = self.users_repo.create_entity(user_data)

        # Act
        retrieved_name = self.users_controller.get_name_by_id(created_user.id)

        # Assert
        self.assertEqual(retrieved_name, created_user.name)

        self.delete_user(created_user)

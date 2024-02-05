from unittest import TestCase
from App.db.models import User
from App.db.repositories.users_repository import UsersRepository
from App.main import initialize_database_and_session
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
        self.assertEqual(retrieved_user, created_user)

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

        # Assert
        self.assertEqual(len(all_users_after) - len(all_users_before), 2)
        self.assertIn(user_1, all_users_after)
        self.assertIn(user_2, all_users_after)

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

        # Act
        self.users_repo.delete_entity(created_user.id)

        # Assert
        self.assertIsNone(self.users_repo.get_entity(created_user.id))

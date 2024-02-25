from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from Backend.db.repositories.shiftBoard_repository import ShiftBoardRepository
from Backend.db.services.shiftBoard_service import ShiftBoardService
from Backend.db.controllers.users_controller import UsersController
from Backend.config.constants import next_sunday


class ShiftBoardController:
    def __init__(self, db: Session):
        self.repository = ShiftBoardRepository(db)
        self.service = ShiftBoardService(self.repository)

    def create_shift_board(self, entity_data: dict):  # TODO: test the error handling
        # Check if the user exists
        user_controller = UsersController(self.repository.db)

        try:
            user_controller.get_entity(entity_data["workplaceID"])
        except NoResultFound:
            raise ValueError(f"User with ID {entity_data['workplaceID']} does not exist")

        # Check if the shift board already exists
        try:
            week_start_date = None

            # Check if the data contains a start day
            if "weekStartDate" in entity_data:
                week_start_date = entity_data["weekStartDate"]
            else:  # If not, calculate the next Sunday
                week_start_date = next_sunday

            self.repository.get_entity(week_start_date, entity_data["workplaceID"])
            raise ValueError(f"Shift board with week start date {entity_data['weekStartDate']} and "
                             f"workplace ID {entity_data['workplaceID']} already exists")
        except NoResultFound:
            pass  # Entity not found, continue creating

        return self.repository.create_entity(entity_data)

    def get_shift_board(self, week_start_day, workplace_id: str):
        return self.repository.get_entity(week_start_day, workplace_id)

    # Probably not needed in the controller
    # def get_all_shift_boards(self):
    #     return self.repository.get_all_entities()

    def update_shift_board(self, week_start_day, workplace_id: str, entity_data: dict):
        return self.repository.update_entity(week_start_day, workplace_id, entity_data)

    def delete_shift_board(self, week_start_day, workplace_id: str):
        return self.repository.delete_entity(week_start_day, workplace_id)

    def publish_shift_board(self, week_start_day, workplace_id: str):
        return self.service.publish_board(week_start_day, workplace_id)

    def unpublish_shift_board(self, week_start_day, workplace_id: str):
        return self.service.unpublish_board(week_start_day, workplace_id)

    def save_shift_board(self, week_start_day, workplace_id: str, content: dict):
        return self.service.save_board(week_start_day, workplace_id, content)

    def get_shift_board_content(self, week_start_day, workplace_id: str):
        return self.service.get_content(week_start_day, workplace_id)

    def get_shift_board_preferences(self, week_start_day, workplace_id: str):
        return self.service.get_preferences(week_start_day, workplace_id)

    def get_all_shift_boards_by_workplace(self, workplace_id: str):
        return self.repository.get_all_shift_boards_by_workplace(workplace_id)

    def get_last_shift_board(self, workplace_id: str):
        return self.service.get_last_board_by_workplace_id(workplace_id)

    def get_content_template_by_preferences(self, preferences, workplace_id) -> dict:
        self.repository.get_content_template_by_preferences(preferences, workplace_id)


def convert_shiftBoard_to_client(shift_board):
    """
    Converts a shift board to a dictionary for client-side use.
    Args:
        shift_board: ShiftBoard object.

    Returns: Dictionary containing shift board data.

    """
    return {
        "weekStartDate": shift_board.weekStartDate,
        "isPublished": shift_board.isPublished,
        "content": shift_board.content,
        "preferences": shift_board.preferences
    }


def convert_shiftBoards_to_client(shift_boards):
    """
    Converts a list of shift boards to a list of dictionaries for client-side use.
    Args:
        shift_boards: List of ShiftBoard objects.

    Returns: List of dictionaries containing shift board data.

    """
    return [convert_shiftBoard_to_client(board) for board in shift_boards]

from Backend.db.repositories.shiftBoard_repository import ShiftBoardRepository


class ShiftBoardService:
    def __init__(self, repository: ShiftBoardRepository):
        self.repository = repository

    def publish_board(self, week_start_day, workplace_id: str):
        # Get the shiftboard
        board = self.repository.get_entity(week_start_day, workplace_id)

        # Check if the shiftboard is already published
        if board.published:
            raise ValueError(f"Board starts at {week_start_day} with workplace_id {workplace_id} already published")

        # Publish the shiftboard
        board.update_entity(week_start_day, workplace_id, {'published': True})

    def unpublish_board(self, week_start_day, workplace_id: str):
        # Get the shiftboard
        board = self.repository.get_entity(week_start_day, workplace_id)

        # Check if the shiftboard is already unpublished
        if not board.published:
            raise ValueError(f"Board starts at {week_start_day} with workplace_id {workplace_id} already unpublished")

        # Unpublish the shiftboard
        board.update_entity(week_start_day, workplace_id, {'published': False})

    def save_board(self, week_start_day, workplace_id: str, content: dict):
        # Get the shiftboard
        board = self.repository.get_entity(week_start_day, workplace_id)

        # Save the shiftboard content
        board.update_entity(week_start_day, workplace_id, {'content': content})

    def get_content(self, week_start_day, workplace_id: str):
        # Get the shiftboard
        board = self.repository.get_entity(week_start_day, workplace_id)

        # Return the shiftboard content
        return board.content

    def get_preferences(self, week_start_day, workplace_id: str):
        # Get the shiftboard
        board = self.repository.get_entity(week_start_day, workplace_id)

        # Return the shiftboard preferences
        return board.preferences

    def get_last_board_by_workplace_id(self, workplace_id: str):
        # Get all shiftboard-s by workplace_id
        all_boards = self.repository.get_all_shift_boards_by_workplace(workplace_id)

        print("len(all_boards): ", len(all_boards))

        # Return the last shiftboard
        return all_boards[-1]

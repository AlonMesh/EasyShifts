from Backend.db.repositories.shiftBoard_repository import ShiftBoardRepository
from Backend.db.services.shiftBoard_service import ShiftBoardService


class ShiftBoardController:
    def __init__(self, repository: ShiftBoardRepository, service: ShiftBoardService):
        self.repository = repository
        self.service = service

    def create_shift_board(self, entity_data: dict):
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

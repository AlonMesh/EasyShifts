from Backend.db.repositories.shiftBoard_repository import ShiftBoardRepository


class ShiftBoardService:
    def __init__(self, repository: ShiftBoardRepository):
        self.repository = repository

    def custom_method(self):
        pass

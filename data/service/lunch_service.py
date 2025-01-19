from entity import Lunch
from dto import LunchDTO
from repository import LunchRepository

class LunchService:
    def __init__(self, lunch_repository):
        self.lunch_repository = lunch_repository

    def _dto_to_entity(self,Lunch:Lunch):
        return LunchDTO(
            id=Lunch.id,
            lunch=Lunch.lunch
        )

    def get_random_menu(self):
        """
        랜덤한 메뉴를 가져오는 서비스 메서드
        """
        try:
            random_menu = self.lunch_repository.get_random_lunch()
            lunch_dto = self._dto_to_entity(random_menu)
            return lunch_dto
        except Exception as e:
            print(f"오류 발생: {e}")
            raise
from data.entity import Lunch
from data.dto import LunchDTO

class LunchService:
    def __init__(self, lunch_repository):
        self.lunch_repository = lunch_repository

    def _entity_to_dto(self, lunch: Lunch):

        return LunchDTO(
            id=lunch.id,
            lunch=lunch.lunch
        )

    def get_random_menu(self) -> LunchDTO:
        """
        랜덤한 메뉴를 가져오는 서비스 메서드
        """
        try:
            random_menu = self.lunch_repository.get_random_lunch()
            lunch_dto = self._entity_to_dto(random_menu)
            return lunch_dto
        except Exception as e:
            print(f"오류 발생: {e}")
            raise
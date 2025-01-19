from entity import Maplebasic,Mapleocid
from dto import  MapleBasicDTO, OcidDTO
from repository import MapleRepository

class LunchService:
    def __init__(self, lunch_repository):
        self.lunch_repository = lunch_repository

    def _maple_basic_entity_to_dto(self,maple_basic:Maplebasic):
        return MapleBasicDTO(
            date=maple_basic.date,
            dojang=maple_basic.dojang,
            level=maple_basic.level,
            union_lv=maple_basic.union_lv,
            unit_class=maple_basic.unit_class,
            guild_name=maple_basic.guild_name
        )
    
    def _maple_basic_dto_to_entity(self,maple_basic_dto:MapleBasicDTO):
        return Maplebasic(
            id=maple_basic_dto.id,
            level = maple_basic_dto.level,
            date = maple_basic_dto.date,
            guild_name = maple_basic_dto.guild_name,
            image = maple_basic_dto.image,
            ocid = maple_basic_dto.ocid,
            unit_class = maple_basic_dto.unit_class,
            union_lv = maple_basic_dto.union_lv,
            dojang = maple_basic_dto.union_lv
        )
    
    def _ocid_entity_to_dto(self,ocid:Mapleocid):

    def _ocid_dto_to_entity(self,ocid_dto:OcidDTO):



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
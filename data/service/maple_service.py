from data.entity import Maplebasic,Mapleocid
from data.dto import  MapleBasicDTO, OcidDTO
from data.repository import MapleRepository

class MapleService:
    def __init__(self, maple_repository:MapleRepository):
        self.maple_repository = maple_repository

    def _maple_basic_entity_to_dto(self,maple_basic:Maplebasic):
        if maple_basic is None:
            return None
        return MapleBasicDTO(
            id=maple_basic.id,
            image=maple_basic.image,
            ocid=maple_basic.ocid,
            date=maple_basic.date,
            dojang=maple_basic.dojang,
            level=maple_basic.level,
            union_lv=maple_basic.union_lv,
            unit_class=maple_basic.unit_class,
            guild_name=maple_basic.guild_name
        )
    
    def _maple_basic_dto_to_entity(self,maple_basic_dto:MapleBasicDTO):
        if maple_basic_dto is None:
            return None
        return Maplebasic(
            id=maple_basic_dto.id,
            level = maple_basic_dto.level,
            date = maple_basic_dto.date,
            guild_name = maple_basic_dto.guild_name,
            image = maple_basic_dto.image,
            ocid = maple_basic_dto.ocid,
            unit_class = maple_basic_dto.unit_class,
            union_lv = maple_basic_dto.union_lv,
            dojang = maple_basic_dto.dojang
        )
    
    def _ocid_entity_to_dto(self,_ocid:Mapleocid):
        if _ocid is None:
            return None
        return OcidDTO(
            id= _ocid.id,
            ocid=_ocid.ocid,
            nickname = _ocid.nickname
        )

    def _ocid_dto_to_entity(self,ocid_dto:OcidDTO):
        if ocid_dto is None:
            return None
        return Mapleocid(
            id=ocid_dto.id,
            ocid=ocid_dto.ocid,
            nickname=ocid_dto.nickname
        )


    def get_ocid(self,nick_name):
        """
        닉네임문자열로 ocid를 불러오는 메서드
        """
        try:
            ocid = self.maple_repository.find_by_nick_name(nick_name)
            ocid_dto = self._ocid_entity_to_dto(ocid)
            return ocid_dto
        except Exception as e:
            print(f"오류 발생: {e}")
    
    def get_maple_basic(self,ocid:str):
        """
        ocid 문자열로 메이플 정보를 불러오는 메서드
        """
        try:
            maple_basic = self.maple_repository.find_by_ocid(ocid)
            maple_basic_dto = self._maple_basic_entity_to_dto(maple_basic)
            return maple_basic_dto
        except Exception as e:
            print(f"오류 발생: {e}")

    def save_ocid(self,ocid_dto:OcidDTO):
        """
            ocid를 저장하는 메서드
        """
        try:
            ocid = self._ocid_dto_to_entity(ocid_dto)
            self.maple_repository.save_ocid(ocid)
        except Exception as e:
            print(f"오류 발생: {e}")

    def save_maple_basic(self,maple_basic_dto:MapleBasicDTO):
        """
            메이플 정보를 저장하는 메서드
        """
        try:
            maple_basic = self._maple_basic_dto_to_entity(maple_basic_dto)
            self.maple_repository.save_maplebasic(maple_basic)
        except Exception as e:
            print(f"오류 발생: {e}")
from entity import Lunch, Maplebasic, Mapleocid
from sqlalchemy.exc import IntegrityError
class MapleRepository:
    def __init__(self, session_provider):
        self._session_provider = session_provider

    def find_by_nick_name(self, nick_name):
        """
        주어진 닉네임을 이용해 ocid를 찾는 함수
        """
        session = self._session_provider.get_session()
        try:
            maple_ocid = session.query().filter(Mapleocid.nickname == nick_name).first()
            return maple_ocid
        finally:
            session.close()

    def get_by_ocid(self, ocid):
        """
        ocid를 활용해 캐릭터를 찾는 함수
        """
        session = self._session_provider.get_session()
        try:
            maple_basic = session.query().filter(Maplebasic.ocid == ocid).first()
            return maple_basic
        finally:
            session.close()

    def save_maplebasic(self, maple_basic):
        """
        데이터베이스에 maple_basic 저장 및 업데이트
        """
        session = self._session_provider.get_session()
        try:
            existing_entry = session.query(Maplebasic).filter_by(ocid=maple_basic.ocid).first()
            if existing_entry:
                existing_entry.level = maple_basic.level
                existing_entry.date = maple_basic.date
                existing_entry.guild_name = maple_basic.guild_name
                existing_entry.image = maple_basic.image
                existing_entry.unit_class = maple_basic.unit_class
                existing_entry.union_lv = maple_basic.union_lv
                existing_entry.dojang = maple_basic.dojang
                print(f"Updated Maplebasic with OCID: {maple_basic.ocid}")
            else:
                session.add(maple_basic)
                print(f"Added new Maplebasic with OCID: {maple_basic.ocid}")
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Integrity error occurred: {e}")
            raise
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise
        finally:
            session.close()

    def save_ocid(self, ocid):
        """
        데이터베이스에 ocid 저장 및 업데이트
        """
        session = self._session_provider.get_session()
        try:
            existing_entry = session.query(Mapleocid).filter_by(ocid=ocid.ocid).first()
            if existing_entry:
                existing_entry.ocid = ocid.ocid
                print(f"Updated OCID: {ocid.ocid}")
            else:
                session.add(ocid)
                print(f"Added new OCID: {ocid.ocid}")
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Integrity error occurred: {e}")
            raise
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise
        finally:
            session.close()
from data.entity import Lunch
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError

class LunchRepository:
    def __init__(self, session_provider):
        self._session_provider = session_provider
    
    
    def get_random_lunch(self):
        """
        랜덤한 메뉴 반환
        """
        session = self._session_provider.get_session()
        try:
            random_entity = session.query(Lunch).order_by(func.random()).first()
            return random_entity
        finally:
            session.close()

    def save_lunch(self,menu):
        """
        데이터베이스에 점심 저장 및 업데이트
        """
        session = self._session_provider.get_session()
        try:
            existing_entry = session.query(Lunch).filter_by(lunch=menu.lunch).first()
            if existing_entry:
                existing_entry.lunch = menu.lunch
                print(f"Updated menu with lunch: {menu.lunch}")
            else:
                session.add(menu)
                print(f"Added new Maplebasic with OCID: {menu.lunch}")
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
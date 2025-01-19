from sqlalchemy import Column, Integer, String
from data.entity.base import Base


class Lunch(Base):
    __tablename__ = "lunch"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lunch = Column(String(50), nullable=False)

    def __repr__(self):
            return f"<Lunch(id={self.id}, name='{self.lunch})'>"
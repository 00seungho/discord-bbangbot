from sqlalchemy import Column, Integer, String
from data.entity.base import Base

class Mapleocid(Base):
    __tablename__ = "mapleocid"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ocid = Column(String(200), nullable=False)
    nickname = Column(String(100), unique=True, nullable=False)
    def __repr__(self):
        return (
            f"<Mapleocid(id={self.id}, ocid={self.ocid}, nickname={self.nickname}"
        )
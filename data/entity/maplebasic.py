from sqlalchemy import Column, Integer, String, Text, DateTime
from data.entity.base import Base

class Maplebasic(Base):
    __tablename__ = "maplebasic"
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False) 
    guild_name = Column(String(100),  nullable=False)
    image = Column(Text, unique=True, nullable=False)
    ocid = Column(String(100), unique=True, nullable=False)
    unit_class = Column(String(100), unique=True, nullable=False)
    union_lv = Column(Integer, unique=True, nullable=False)
    dojang = Column(Integer, unique=True, nullable=False)
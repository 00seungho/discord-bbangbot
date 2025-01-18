from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Mapleocid(Base):
    __tablename__ = "mapleocid"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ocid = Column(String(200), nullable=False)
    nickname = Column(String(100), unique=True, nullable=False)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Lunch(Base):
    __tablename__ = "lunch"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lunch = Column(String(50), nullable=False)

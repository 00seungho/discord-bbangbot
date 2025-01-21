from sqlalchemy import Column, Integer, String, Text, DateTime
from data.entity.base import Base

class Maplebasic(Base):
    __tablename__ = "maplebasic"
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False) 
    guild_name = Column(String(100),  nullable=False)
    image = Column(Text, nullable=False)
    ocid = Column(String(100), nullable=False)
    unit_class = Column(String(100),  nullable=False)
    union_lv = Column(Integer, nullable=False)
    dojang = Column(Integer,  nullable=False)
    def __repr__(self):
        return (
            f"<Maplebasic(id={self.id}, level={self.level}, date={self.date}, "
            f"guild_name='{self.guild_name}', image='{self.image}', "
            f"ocid='{self.ocid}', unit_class='{self.unit_class}', "
            f"union_lv={self.union_lv}, dojang={self.dojang})>"
        )
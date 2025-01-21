from pydantic import BaseModel
from datetime import datetime

class MapleBasicDTO(BaseModel):
    id: int = None
    unit_class: str
    level:int
    union_lv:int
    dojang:int
    date:datetime
    image:str
    guild_name:str
    ocid:str
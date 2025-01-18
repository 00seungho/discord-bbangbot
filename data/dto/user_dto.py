from pydantic import BaseModel
from datetime import datetime

class MapleBasicDTO(BaseModel):
    id: int
    nick_name: str
    unit_class: str
    level:int
    union_lv:int
    dojang:int
    date:datetime
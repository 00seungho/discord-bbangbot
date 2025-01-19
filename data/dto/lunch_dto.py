from pydantic import BaseModel

class LunchDTO(BaseModel):
    id: int
    lunch: str

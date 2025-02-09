from pydantic import BaseModel

class LOLPlayerDTO(BaseModel):
    id: int
    lunch: str
from pydantic import BaseModel

class OcidDTO(BaseModel):
    id: int = None
    ocid: str
    nickname: str
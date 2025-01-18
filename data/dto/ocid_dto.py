from pydantic import BaseModel

class OcidDTO(BaseModel):
    id: int
    ocid: str

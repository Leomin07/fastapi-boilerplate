from typing import Optional
from pydantic import BaseModel


class create_pet_schema(BaseModel):
    name: str
    description: Optional[str]
    price: int
    image: Optional[str] = None


class update_pet_schema(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image: Optional[str] = None

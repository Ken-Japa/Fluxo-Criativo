# backend/app/schemas/item.py
"""
Schemas Pydantic para validação de dados de entrada e saída.
"""
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemInDBBase(ItemBase):
    id: int

    class Config:
        from_attributes = True

class Item(ItemInDBBase):
    pass
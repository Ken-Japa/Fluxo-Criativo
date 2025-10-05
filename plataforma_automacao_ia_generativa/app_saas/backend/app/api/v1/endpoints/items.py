# backend/app/api/v1/endpoints/items.py
"""
Endpoints da API para gerenciamento de itens (exemplo).
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/items/")
async def read_items():
    return [{"item_id": "foo", "name": "Foo"}, {"item_id": "bar", "name": "Bar"}]
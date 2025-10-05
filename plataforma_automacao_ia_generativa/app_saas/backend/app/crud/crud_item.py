# backend/app/crud/crud_item.py
"""
Operações CRUD (Create, Read, Update, Delete) para o modelo Item.
"""
from sqlalchemy.orm import Session

# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

class CRUDItem:
    def get(self, db: Session, id: int):
        # return db.query(Item).filter(Item.id == id).first()
        pass

    def create(self, db: Session, obj_in):
        # db_obj = Item(**obj_in.dict())
        # db.add(db_obj)
        # db.commit()
        # db.refresh(db_obj)
        # return db_obj
        pass

crud_item = CRUDItem()
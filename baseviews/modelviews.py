from sqlalchemy.orm import Session, DeclarativeBase
from fastapi import HTTPException, status


class ModelViewSet():
    def __init__(self, db: Session, model: DeclarativeBase):
        self.db = db
        self.model = model
    
    def get(self, obj_id):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()

        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj
    
    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, data: dict):
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj_id: int, data: dict):
        obj = self.get(obj_id=obj_id)
        for k, v in data.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, obj_id: int):
        obj = self.get(obj_id=obj_id)
        self.db.delete(obj)
        self.db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
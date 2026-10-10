from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.connection import get_db
from backend.models import domain as models

# Very basic schemas inline for speed
from pydantic import BaseModel
from typing import Optional

class EntityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    review_status: Optional[str] = None

class EntityReview(BaseModel):
    status: str # "confirmed", "rejected", "pending"

router = APIRouter()

@router.get("/projects/{project_id}/entities")
def get_entities(project_id: int, db: Session = Depends(get_db)):
    entities = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.project_id == project_id).all()
    return entities

@router.get("/entities/{entity_id}")
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    entity = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.patch("/entities/{entity_id}")
def update_entity(entity_id: int, entity_update: EntityUpdate, db: Session = Depends(get_db)):
    entity = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    update_data = entity_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entity, key, value)
        
    db.commit()
    db.refresh(entity)
    return entity

@router.post("/entities/{entity_id}/review")
def review_entity(entity_id: int, review: EntityReview, db: Session = Depends(get_db)):
    entity = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    entity.review_status = review.status
    db.commit()
    db.refresh(entity)
    return entity

@router.get("/projects/{project_id}/relationships")
def get_relationships(project_id: int, db: Session = Depends(get_db)):
    rels = db.query(models.ArchitectureRelationship).filter(models.ArchitectureRelationship.project_id == project_id).all()
    return rels

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models import domain as models

from pydantic import BaseModel

class ComparisonCreate(BaseModel):
    baseline_document_id: int
    comparison_document_id: int

router = APIRouter()

@router.post("/projects/{project_id}/comparisons")
def create_comparison(project_id: int, comp: ComparisonCreate, db: Session = Depends(get_db)):
    db_comp = models.DocumentComparison(
        project_id=project_id,
        baseline_document_id=comp.baseline_document_id,
        comparison_document_id=comp.comparison_document_id,
        status="completed",
        results_json="""{"added": [], "removed": [], "modified": []}""",
        created_by=None
    )
    db.add(db_comp)
    db.commit()
    db.refresh(db_comp)
    return db_comp

@router.get("/comparisons/{comparison_id}")
def get_comparison(comparison_id: int, db: Session = Depends(get_db)):
    comp = db.query(models.DocumentComparison).filter(models.DocumentComparison.id == comparison_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return comp

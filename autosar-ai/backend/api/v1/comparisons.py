import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database.connection import get_db
from backend.models import domain as models

from pydantic import BaseModel

class ComparisonCreate(BaseModel):
    baseline_document_id: int
    comparison_document_id: int

router = APIRouter()

@router.get("/projects/{project_id}/comparisons")
def get_project_comparisons(project_id: int, db: Session = Depends(get_db)):
    comps = db.query(models.DocumentComparison).filter(
        models.DocumentComparison.project_id == project_id
    ).order_by(models.DocumentComparison.created_at.desc()).all()
    
    # Enrich with document names
    doc_cache = {}
    enriched = []
    for c in comps:
        for d_id in [c.baseline_document_id, c.comparison_document_id]:
            if d_id not in doc_cache:
                doc = db.query(models.Document).filter(models.Document.id == d_id).first()
                doc_cache[d_id] = doc.original_filename if doc else f"Doc #{d_id}"
                
        try:
            results = json.loads(c.results_json or "{}")
        except:
            results = {"added": [], "removed": [], "modified": []}
            
        enriched.append({
            "id": c.id,
            "project_id": c.project_id,
            "baseline_document_id": c.baseline_document_id,
            "baseline_document_name": doc_cache.get(c.baseline_document_id, ""),
            "comparison_document_id": c.comparison_document_id,
            "comparison_document_name": doc_cache.get(c.comparison_document_id, ""),
            "status": c.status,
            "added_count": len(results.get("added", [])),
            "removed_count": len(results.get("removed", [])),
            "modified_count": len(results.get("modified", [])),
            "created_at": str(c.created_at),
            "results_json": c.results_json
        })
    return enriched

@router.post("/projects/{project_id}/comparisons")
def create_comparison(project_id: int, comp: ComparisonCreate, db: Session = Depends(get_db)):
    if comp.baseline_document_id == comp.comparison_document_id:
        raise HTTPException(status_code=400, detail="Baseline and comparison documents must be different.")
        
    doc_base = db.query(models.Document).filter(models.Document.id == comp.baseline_document_id, models.Document.project_id == project_id).first()
    doc_comp = db.query(models.Document).filter(models.Document.id == comp.comparison_document_id, models.Document.project_id == project_id).first()
    
    if not doc_base or not doc_comp:
        raise HTTPException(status_code=404, detail="One or both selected documents not found in project.")

    # Fetch architectural entities
    base_entities = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.document_id == comp.baseline_document_id).all()
    comp_entities = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.document_id == comp.comparison_document_id).all()

    base_map = {(e.entity_type, e.name): e for e in base_entities}
    comp_map = {(e.entity_type, e.name): e for e in comp_entities}

    added = []
    removed = []
    modified = []

    for key, ent in comp_map.items():
        if key not in base_map:
            added.append({
                "type": ent.entity_type,
                "name": ent.name,
                "description": ent.description or "",
                "source_page": ent.source_page or 1,
                "source_excerpt": ent.source_excerpt or ""
            })
        else:
            base_ent = base_map[key]
            # Check if excerpt or description changed
            if (ent.source_excerpt or "") != (base_ent.source_excerpt or ""):
                modified.append({
                    "type": ent.entity_type,
                    "name": ent.name,
                    "baseline_excerpt": base_ent.source_excerpt or "",
                    "comparison_excerpt": ent.source_excerpt or "",
                    "baseline_page": base_ent.source_page or 1,
                    "comparison_page": ent.source_page or 1
                })

    for key, ent in base_map.items():
        if key not in comp_map:
            removed.append({
                "type": ent.entity_type,
                "name": ent.name,
                "description": ent.description or "",
                "source_page": ent.source_page or 1,
                "source_excerpt": ent.source_excerpt or ""
            })

    results_data = {
        "baseline_filename": doc_base.original_filename,
        "comparison_filename": doc_comp.original_filename,
        "added": added,
        "removed": removed,
        "modified": modified
    }

    db_comp = models.DocumentComparison(
        project_id=project_id,
        baseline_document_id=comp.baseline_document_id,
        comparison_document_id=comp.comparison_document_id,
        status="completed",
        results_json=json.dumps(results_data),
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

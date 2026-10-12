import os
import csv
import json
import io
import time
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models import domain as models
from backend.core.config import settings
from pydantic import BaseModel

def sanitize_csv_cell(val: Any) -> str:
    """Protects against spreadsheet formula injection vulnerabilities."""
    if val is None:
        return ""
    text = str(val).strip()
    if text and text[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + text
    return text

class ReportCreate(BaseModel):
    report_type: str
    format: str

router = APIRouter()

@router.get("/projects/{project_id}/reports")
def get_reports(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.project_id == project_id).order_by(models.Report.created_at.desc()).all()

@router.post("/projects/{project_id}/reports")
def create_report(project_id: int, report_req: ReportCreate, db: Session = Depends(get_db)):
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    fmt = report_req.format.lower()
    ts = int(time.time())
    safe_type = report_req.report_type.replace(" ", "_").lower()
    filename = f"report_proj{project_id}_{safe_type}_{ts}.{fmt}"
    filepath = os.path.join(settings.EXPORT_DIR, filename)

    if report_req.report_type == "Architecture Summary":
        entities = db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.project_id == project_id).all()
        
        if fmt == "json":
            data = [{
                "id": e.id,
                "type": e.entity_type,
                "name": e.name,
                "review_status": e.review_status,
                "source_page": e.source_page,
                "description": e.description,
                "source_excerpt": e.source_excerpt
            } for e in entities]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"project_id": project_id, "report_type": report_req.report_type, "entities": data}, f, indent=2)
                
        elif fmt == "csv":
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Entity Type", "Name", "Review Status", "Source Page", "Description", "Excerpt"])
                for e in entities:
                    writer.writerow([
                        e.id,
                        sanitize_csv_cell(e.entity_type),
                        sanitize_csv_cell(e.name),
                        sanitize_csv_cell(e.review_status),
                        e.source_page or "",
                        sanitize_csv_cell(e.description),
                        sanitize_csv_cell(e.source_excerpt)
                    ])
        else: # text / pdf-compatible report
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== AUTOSAR AI — ARCHITECTURE SUMMARY REPORT ===\n")
                f.write(f"Project ID: {project_id}\n")
                f.write(f"Total Extracted Entities: {len(entities)}\n\n")
                for e in entities:
                    f.write(f"[{e.entity_type}] {e.name} (Status: {e.review_status}, Page: {e.source_page})\n")
                    if e.source_excerpt:
                        f.write(f"  Excerpt: {e.source_excerpt}\n")
                f.write("\n=== END OF REPORT ===\n")

    elif report_req.report_type == "Findings Report":
        findings = db.query(models.Finding).filter(models.Finding.project_id == project_id).all()
        
        if fmt == "json":
            data = [{
                "id": fnd.id,
                "type": fnd.finding_type,
                "severity": fnd.severity,
                "status": fnd.review_status,
                "description": fnd.description,
                "comments": fnd.reviewer_comments
            } for fnd in findings]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"project_id": project_id, "report_type": report_req.report_type, "findings": data}, f, indent=2)
                
        elif fmt == "csv":
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Finding Type", "Severity", "Status", "Description", "Comments"])
                for fnd in findings:
                    writer.writerow([
                        fnd.id,
                        sanitize_csv_cell(fnd.finding_type),
                        sanitize_csv_cell(fnd.severity),
                        sanitize_csv_cell(fnd.review_status),
                        sanitize_csv_cell(fnd.description),
                        sanitize_csv_cell(fnd.reviewer_comments)
                    ])
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== AUTOSAR AI — FINDINGS & VALIDATION REPORT ===\n")
                f.write(f"Project ID: {project_id}\n")
                f.write(f"Total Rule Findings: {len(findings)}\n\n")
                for fnd in findings:
                    f.write(f"[{fnd.severity}] {fnd.finding_type} (Status: {fnd.review_status})\n")
                    f.write(f"  Description: {fnd.description}\n")
                f.write("\n=== END OF REPORT ===\n")

    else: # Dependency Matrix or other
        rels = db.query(models.ArchitectureRelationship).filter(models.ArchitectureRelationship.project_id == project_id).all()
        if fmt == "json":
            data = [{"id": r.id, "type": r.relationship_type, "status": r.review_status} for r in rels]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"project_id": project_id, "report_type": report_req.report_type, "relationships": data}, f, indent=2)
        elif fmt == "csv":
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Relationship Type", "Status"])
                for r in rels:
                    writer.writerow([r.id, sanitize_csv_cell(r.relationship_type), sanitize_csv_cell(r.review_status)])
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== AUTOSAR AI — DEPENDENCY MATRIX ===\nTotal Relationships: {len(rels)}\n")

    db_report = models.Report(
        project_id=project_id,
        report_type=report_req.report_type,
        format=report_req.format.upper(),
        storage_path=filepath,
        generated_by=None
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/reports/{report_id}/download")
def download_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    if not os.path.exists(report.storage_path):
        raise HTTPException(status_code=404, detail="Report file not found on disk")
        
    return FileResponse(report.storage_path, filename=os.path.basename(report.storage_path))

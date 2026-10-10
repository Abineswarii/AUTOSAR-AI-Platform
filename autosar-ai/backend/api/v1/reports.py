from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models import domain as models
from backend.core.config import settings

import os
from pydantic import BaseModel

class ReportCreate(BaseModel):
    report_type: str
    format: str

router = APIRouter()

@router.get("/projects/{project_id}/reports")
def get_reports(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.project_id == project_id).all()

@router.post("/projects/{project_id}/reports")
def create_report(project_id: int, report_req: ReportCreate, db: Session = Depends(get_db)):
    # Mocking report generation
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    filename = f"report_{project_id}_{report_req.report_type}.{report_req.format}"
    filepath = os.path.join(settings.EXPORT_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(f"Report for Project {project_id}\nType: {report_req.report_type}\nFormat: {report_req.format}")

    db_report = models.Report(
        project_id=project_id,
        report_type=report_req.report_type,
        format=report_req.format,
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

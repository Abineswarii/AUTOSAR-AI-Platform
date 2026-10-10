from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import hashlib

from backend.database.connection import get_db
from backend.models import domain as models
from backend.schemas import domain as schemas
from backend.core.config import settings
from backend.services.document_service import process_document

router = APIRouter()

@router.get("/projects/{project_id}/documents", response_model=List[schemas.DocumentResponse])
def get_documents(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.project_id == project_id).all()

@router.post("/projects/{project_id}/documents", response_model=schemas.DocumentResponse)
def upload_document(project_id: int, background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Check project exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Calculate sha256 while saving
    sha256_hash = hashlib.sha256()
    file_path = os.path.join(settings.UPLOAD_DIR, f"{project_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        while chunk := file.file.read(8192):
            sha256_hash.update(chunk)
            buffer.write(chunk)
            
    # Check if this exact file was already uploaded to this project
    file_hash = sha256_hash.hexdigest()
    existing_doc = db.query(models.Document).filter(
        models.Document.project_id == project_id,
        models.Document.sha256_hash == file_hash
    ).first()
    
    if existing_doc:
        os.remove(file_path)
        return existing_doc
        
    db_document = models.Document(
        project_id=project_id,
        original_filename=file.filename,
        storage_path=file_path,
        sha256_hash=file_hash,
        status="UPLOADED"
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Process in background
    background_tasks.add_task(process_document, db_document.id, db)
    
    return db_document

@router.get("/documents/{document_id}", response_model=schemas.DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/documents/{document_id}/status")
def get_document_status(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": doc.id, "status": doc.status, "error_message": doc.error_message}

@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete chunks
    db.query(models.DocumentChunk).filter(models.DocumentChunk.document_id == document_id).delete()
    
    # Delete file
    if os.path.exists(doc.storage_path):
        os.remove(doc.storage_path)
        
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}

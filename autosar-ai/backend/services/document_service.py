import time
from sqlalchemy.orm import Session
from backend.models import domain as models

def process_document(document_id: int, db: Session):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        return

    try:
        doc.status = "EXTRACTING"
        db.commit()
        
        # Simulate processing for now until actual PyMuPDF processing is implemented
        time.sleep(2)
        
        doc.status = "READY"
        doc.page_count = 10 # Placeholder
        db.commit()
        
    except Exception as e:
        doc.status = "FAILED"
        doc.error_message = str(e)
        db.commit()

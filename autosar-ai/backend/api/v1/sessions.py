from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.connection import get_db
from backend.models import domain as models
from backend.schemas import domain as schemas
from backend.core.config import settings
from backend.services.llm_service import ask_question
from backend.services.vector_store_service import search_chunks

router = APIRouter()

# Simple schema definitions inline to avoid over-complicating domain schemas
from pydantic import BaseModel
class AskQuery(BaseModel):
    query: str
    document_ids: List[int] = []

@router.post("/projects/{project_id}/ask")
def ask_assistant(project_id: int, query: AskQuery, db: Session = Depends(get_db)):
    # Check project
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Search in vector store
    results = search_chunks(
        project_id=project_id, 
        query=query.query, 
        top_k=getattr(settings, "TOP_K", 5),
        document_ids=query.document_ids if query.document_ids else None
    )
    
    # Context generation and citations
    context = ""
    citations = []
    
    # Cache document names
    doc_name_cache = {}
    
    if results and results.get('documents') and len(results['documents'][0]) > 0:
        for idx, text_passage in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][idx]
            doc_id = metadata.get('document_id')
            page_start = metadata.get('page_start', 1)
            page_end = metadata.get('page_end', 1)
            
            if doc_id not in doc_name_cache:
                doc_record = db.query(models.Document).filter(models.Document.id == doc_id).first()
                doc_name_cache[doc_id] = doc_record.original_filename if doc_record else f"Doc #{doc_id}"
                
            doc_name = doc_name_cache[doc_id]
            context += f"Document: {doc_name} (Page {page_start}-{page_end})\nExcerpt: {text_passage}\n\n"
            citations.append({
                "document_id": doc_id,
                "document_name": doc_name,
                "page_start": page_start,
                "page_end": page_end,
                "content": text_passage
            })

    # Ask LLM (Ollama or configured provider)
    answer = ask_question(query.query, context)
    
    # Record session
    session = models.AnalysisSession(project_id=project_id, title=query.query[:50], user_id=None)
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Record user message
    msg = models.AnalysisMessage(
        session_id=session.id, 
        role="user", 
        content=query.query
    )
    db.add(msg)
    
    # Record assistant message
    import json
    msg_assist = models.AnalysisMessage(
        session_id=session.id, 
        role="assistant", 
        content=answer,
        citations_json=json.dumps(citations)
    )
    db.add(msg_assist)
    db.commit()

    return {
        "answer": answer,
        "citations": citations,
        "session_id": session.id
    }

@router.get("/projects/{project_id}/sessions")
def get_project_sessions(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.AnalysisSession).filter(models.AnalysisSession.project_id == project_id).order_by(models.AnalysisSession.created_at.desc()).all()

@router.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    return db.query(models.AnalysisMessage).filter(models.AnalysisMessage.session_id == session_id).order_by(models.AnalysisMessage.created_at.asc()).all()

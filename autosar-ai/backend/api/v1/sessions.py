from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.connection import get_db
from backend.models import domain as models
from backend.schemas import domain as schemas
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
    results = search_chunks(project_id=project_id, query=query.query)
    
    # Simple context generation
    context = ""
    citations = []
    if results and results['documents'] and len(results['documents'][0]) > 0:
        for idx, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][idx]
            context += f"Document ID: {metadata['document_id']}\nContent: {doc}\n\n"
            citations.append({
                "document_id": metadata["document_id"],
                "content": doc,
                "metadata": metadata
            })

    # Ask LLM
    answer = ask_question(query.query, context)
    
    # Record session
    session = models.AnalysisSession(project_id=project_id, title=query.query[:50], user_id=None)
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Record message
    msg = models.AnalysisMessage(
        session_id=session.id, 
        role="user", 
        content=query.query
    )
    db.add(msg)
    
    msg_assist = models.AnalysisMessage(
        session_id=session.id, 
        role="assistant", 
        content=answer,
        citations_json=str(citations)
    )
    db.add(msg_assist)
    db.commit()

    return {
        "answer": answer,
        "citations": citations,
        "session_id": session.id
    }

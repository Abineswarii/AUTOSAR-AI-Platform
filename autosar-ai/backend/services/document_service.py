import os
import re
import hashlib
import json
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import pymupdf  # PyMuPDF

from backend.database.connection import SessionLocal
from backend.models import domain as models
from backend.core.config import settings
from backend.services.vector_store_service import add_chunks, delete_chunks_by_document

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    """Chunks text into overlapping blocks."""
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += (chunk_size - overlap)
        if start >= len(text):
            break
    return chunks

def extract_entities_from_text(text: str, page_num: int) -> List[Dict[str, Any]]:
    """Identifies AUTOSAR architectural entities using engineering patterns."""
    entities = []
    
    # 1. Software Components
    swc_pattern = r'\b([A-Z][A-Za-z0-9_]*(?:_SWC|Component|Controller|Manager|Handler|Sensor|Actuator|ECU))\b'
    for match in re.finditer(swc_pattern, text):
        name = match.group(1)
        start_pos = max(0, match.start() - 60)
        end_pos = min(len(text), match.end() + 60)
        excerpt = text[start_pos:end_pos].strip()
        entities.append({
            "type": "Software Component",
            "name": name,
            "description": f"Extracted Software Component identified on page {page_num}",
            "source_page": page_num,
            "source_excerpt": excerpt,
            "confidence": 0.92
        })
        
    # 2. Runnables
    runnable_pattern = r'\b(Runnable_[A-Za-z0-9_]+|[A-Za-z0-9_]+_Runnable|run_[A-Za-z0-9_]+)\b'
    for match in re.finditer(runnable_pattern, text):
        name = match.group(1)
        start_pos = max(0, match.start() - 60)
        end_pos = min(len(text), match.end() + 60)
        excerpt = text[start_pos:end_pos].strip()
        entities.append({
            "type": "Runnable",
            "name": name,
            "description": f"Extracted Runnable task identified on page {page_num}",
            "source_page": page_num,
            "source_excerpt": excerpt,
            "confidence": 0.90
        })

    # 3. Interfaces
    if_pattern = r'\b([A-Za-z0-9_]+_IF|[A-Za-z0-9_]+_Interface|SenderReceiver_[A-Za-z0-9_]+|ClientServer_[A-Za-z0-9_]+)\b'
    for match in re.finditer(if_pattern, text):
        name = match.group(1)
        start_pos = max(0, match.start() - 60)
        end_pos = min(len(text), match.end() + 60)
        excerpt = text[start_pos:end_pos].strip()
        entities.append({
            "type": "Interface",
            "name": name,
            "description": f"Extracted AUTOSAR Interface specification identified on page {page_num}",
            "source_page": page_num,
            "source_excerpt": excerpt,
            "confidence": 0.88
        })
        
    return entities

def run_enterprise_rule_checks(db: Session, project_id: int, document_id: int, full_text: str):
    """
    Applies enterprise architectural validation rules:
    - Circular dependency detection
    - Insecure IPC verification
    - Missing array bounds checks
    """
    findings = []
    
    # Check 1: Insecure IPC or raw pointers
    insecure_patterns = [
        (r'(shared\s+memory|raw\s+pointer|direct\s+memory\s+access|bypassing\s+RTE)', "High", "Insecure IPC / Direct Memory Access: Document references unmanaged inter-process memory communication bypassing AUTOSAR RTE safeguards."),
        (r'(unauthenticated\s+CAN|cleartext\s+IPC|unencrypted\s+bus)', "High", "Insecure Bus Communication: Unauthenticated communication pathway detected without SecOC validation."),
    ]
    for pattern, severity, desc in insecure_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            start_pos = max(0, match.start() - 50)
            end_pos = min(len(full_text), match.end() + 50)
            evidence = full_text[start_pos:end_pos].strip()
            findings.append(models.Finding(
                project_id=project_id,
                document_id=document_id,
                finding_type="Insecure IPC",
                severity=severity,
                description=desc,
                evidence_json=json.dumps({"excerpt": evidence, "matched": match.group(0)}),
                review_status="open"
            ))

    # Check 2: Missing boundary definitions on arrays
    array_matches = re.finditer(r'(\b\w+\s*\[\s*\]|\bunbounded\s+array|\bvariable\s+length\s+buffer)', full_text, re.IGNORECASE)
    for match in array_matches:
        start_pos = max(0, match.start() - 50)
        end_pos = min(len(full_text), match.end() + 50)
        evidence = full_text[start_pos:end_pos].strip()
        findings.append(models.Finding(
            project_id=project_id,
            document_id=document_id,
            finding_type="Missing Boundary Definition",
            severity="Medium",
            description="Missing boundary definition: Unbounded array or dynamic buffer detected without explicit AUTOSAR upper-bound constraint.",
            evidence_json=json.dumps({"excerpt": evidence, "matched": match.group(0)}),
            review_status="open"
        ))
        break # Flag once per document to avoid duplicate alert flooding

    # Check 3: Circular Dependencies in entities
    entities = db.query(models.ArchitectureEntity).filter(
        models.ArchitectureEntity.document_id == document_id,
        models.ArchitectureEntity.entity_type == "Software Component"
    ).all()
    
    # If multiple SWCs mention each other in excerpts, flag potential circular coupling
    if len(entities) >= 2:
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                e1, e2 = entities[i], entities[j]
                if e1.name in (e2.source_excerpt or "") and e2.name in (e1.source_excerpt or ""):
                    findings.append(models.Finding(
                        project_id=project_id,
                        document_id=document_id,
                        finding_type="Circular Dependency",
                        severity="High",
                        description=f"Potential circular dependency detected between Software Components '{e1.name}' and '{e2.name}'.",
                        evidence_json=json.dumps({"component_a": e1.name, "component_b": e2.name}),
                        review_status="open"
                    ))

    for f in findings:
        db.add(f)
    db.commit()

def process_document(document_id: int, db: Optional[Session] = None):
    """
    Full document ingestion pipeline:
    1. Parse PDF pages using PyMuPDF
    2. Extract text & preserve page numbers
    3. Generate chunks & compute hashes
    4. Index chunks into ChromaDB
    5. Extract architectural entities
    6. Execute enterprise rule checks & record findings
    7. Update document status to READY
    """
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        doc = db.query(models.Document).filter(models.Document.id == document_id).first()
        if not doc:
            return

        doc.status = "PROCESSING"
        doc.error_message = None
        db.commit()

        if not os.path.exists(doc.storage_path):
            raise FileNotFoundError(f"Document file not found at: {doc.storage_path}")

        # Clean existing chunks & vectors if reprocessing
        db.query(models.DocumentChunk).filter(models.DocumentChunk.document_id == document_id).delete()
        db.query(models.ArchitectureEntity).filter(models.ArchitectureEntity.document_id == document_id).delete()
        db.query(models.ArchitectureRelationship).filter(models.ArchitectureRelationship.document_id == document_id).delete()
        db.query(models.Finding).filter(models.Finding.document_id == document_id).delete()
        delete_chunks_by_document(doc.project_id, document_id)
        db.commit()

        # Open PDF
        pdf_doc = pymupdf.open(doc.storage_path)
        doc.page_count = len(pdf_doc)
        
        all_chunks_for_db = []
        all_chunks_for_vector = []
        full_document_text = ""
        chunk_index = 0
        extracted_entities_all = []

        for page_idx in range(len(pdf_doc)):
            page_num = page_idx + 1  # 1-indexed
            page_obj = pdf_doc[page_idx]
            page_text = page_obj.get_text()
            full_document_text += f"\n--- Page {page_num} ---\n" + page_text
            
            # Extract entities from page text
            page_entities = extract_entities_from_text(page_text, page_num)
            extracted_entities_all.extend(page_entities)
            
            # Chunk page text
            page_chunks = chunk_text(
                page_text, 
                chunk_size=getattr(settings, "CHUNK_SIZE", 1000), 
                overlap=getattr(settings, "CHUNK_OVERLAP", 150)
            )
            
            for c_text in page_chunks:
                c_hash = hashlib.sha256(c_text.encode('utf-8')).hexdigest()
                db_chunk = models.DocumentChunk(
                    project_id=doc.project_id,
                    document_id=doc.id,
                    chunk_index=chunk_index,
                    page_start=page_num,
                    page_end=page_num,
                    text_content=c_text,
                    content_hash=c_hash
                )
                all_chunks_for_db.append(db_chunk)
                all_chunks_for_vector.append({
                    "chunk_index": chunk_index,
                    "text_content": c_text,
                    "page_start": page_num,
                    "page_end": page_num
                })
                chunk_index += 1

        # Bulk save chunks
        if all_chunks_for_db:
            db.add_all(all_chunks_for_db)
            db.commit()
            
        # Index in ChromaDB
        if all_chunks_for_vector:
            add_chunks(doc.project_id, doc.id, all_chunks_for_vector)

        # Deduplicate & insert extracted entities
        seen_entities = set()
        db_entities = []
        for ent in extracted_entities_all:
            key = (ent["type"], ent["name"])
            if key not in seen_entities:
                seen_entities.add(key)
                db_ent = models.ArchitectureEntity(
                    project_id=doc.project_id,
                    document_id=doc.id,
                    entity_type=ent["type"],
                    name=ent["name"],
                    description=ent["description"],
                    source_page=ent["source_page"],
                    source_excerpt=ent["source_excerpt"],
                    extraction_method="regex_heuristic",
                    confidence=ent["confidence"],
                    review_status="pending"
                )
                db_entities.append(db_ent)

        if db_entities:
            db.add_all(db_entities)
            db.commit()

        # Run enterprise rule validation on the extracted content
        run_enterprise_rule_checks(db, doc.project_id, doc.id, full_document_text)

        pdf_doc.close()
        
        # Mark document as READY
        doc.status = "READY"
        doc.error_message = None
        db.commit()

    except Exception as e:
        if doc:
            doc.status = "FAILED"
            doc.error_message = str(e)
            db.commit()
    finally:
        if own_session:
            db.close()

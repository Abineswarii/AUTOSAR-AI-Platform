import os
import chromadb
from backend.core.config import settings

# Initialize ChromaDB client
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_DIR)

def get_collection(project_id: int):
    collection_name = f"project_{project_id}"
    return chroma_client.get_or_create_collection(name=collection_name)

def add_chunks(project_id: int, document_id: int, chunks: list[dict]):
    collection = get_collection(project_id)
    
    ids = []
    documents = []
    metadatas = []
    
    for chunk in chunks:
        ids.append(f"{document_id}_{chunk['chunk_index']}")
        documents.append(chunk['text_content'])
        metadatas.append({
            "document_id": document_id,
            "chunk_index": chunk['chunk_index'],
            "page_start": chunk.get('page_start', 0),
            "page_end": chunk.get('page_end', 0)
        })
        
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def search_chunks(project_id: int, query: str, top_k: int = 5):
    collection = get_collection(project_id)
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results

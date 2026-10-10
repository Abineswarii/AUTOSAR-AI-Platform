from fastapi import FastAPI
from backend.core.config import settings
from backend.database.connection import engine
from backend.database.base import Base
from backend.models import domain

# Create tables for initial setup (in production use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AUTOSAR HLD Document Analysis Assistant"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/api/v1/health")
def health_check_v1():
    return {"status": "ok", "app": settings.APP_NAME, "version": "v1"}

from backend.api.v1 import projects, documents, sessions, entities, comparisons, findings, reports

app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(entities.router, prefix="/api/v1", tags=["entities"])
app.include_router(comparisons.router, prefix="/api/v1", tags=["comparisons"])
app.include_router(findings.router, prefix="/api/v1", tags=["findings"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

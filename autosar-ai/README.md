# AUTOSAR AI — High-Level Design Document Intelligence Platform

AUTOSAR AI is an AI-assisted application that helps automotive engineering teams analyze High-Level Design (HLD) documents.

## Features
- **Document Management**: Upload and process PDF HLD documents.
- **AI Assistant**: Ask natural-language questions grounded in document evidence.
- **Architecture Extraction**: Extract components, interfaces, ports, and dependencies.
- **Comparison**: Compare two versions of an HLD document to identify changes.
- **Findings and Validation**: Run rule-based checks for potential inconsistencies.
- **Reports**: Generate document summaries and architecture inventories.

## Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

## Setup Instructions

1. Clone or navigate to the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Copy `.env.example` to `.env` and fill in the required variables.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Start the Streamlit frontend (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

## Docker Deployment
   ```bash
   docker-compose up --build
   ```

## Testing
Run the test suite using pytest:
```bash
pytest tests/
```

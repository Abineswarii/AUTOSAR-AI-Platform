# AUTOSAR AI — REST API Documentation

## 1. Overview
The **AUTOSAR AI** backend is implemented using **FastAPI** running on port 8000. All primary API routes are prefixed with `/api/v1/` and return typed JSON responses with standard HTTP status codes.

---

## 2. Complete API Endpoint Catalog

| HTTP Method | Route Path | Subsystem | Description | Request Body / Parameters | Response Code |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Core | Root system health check | None | `200 OK` |
| `GET` | `/api/v1/health` | Core | API v1 version health check | None | `200 OK` |
| `GET` | `/api/v1/projects/` | Projects | List all workspace projects | None | `200 OK` |
| `POST` | `/api/v1/projects/` | Projects | Create new project workspace | `ProjectCreate` (name, description) | `200 OK` |
| `GET` | `/api/v1/projects/{id}` | Projects | Get project details by ID | `id` path param | `200 OK` / `404` |
| `GET` | `/api/v1/projects/{id}/metrics` | Projects | Telemetry counts (docs, entities, findings) | `id` path param | `200 OK` |
| `GET` | `/api/v1/projects/{id}/documents` | Documents | List all specification documents in project | `id` path param | `200 OK` |
| `POST` | `/api/v1/projects/{id}/documents` | Documents | Upload & ingest specification PDF | Form: `file` (.pdf), `version_label`, `governance_state` | `200 OK` / `400` / `413` |
| `GET` | `/api/v1/documents/{id}` | Documents | Get document metadata by ID | `id` path param | `200 OK` / `404` |
| `GET` | `/api/v1/documents/{id}/status` | Documents | Check processing / indexing status | `id` path param | `200 OK` / `404` |
| `PATCH` | `/api/v1/documents/{id}/governance` | Documents | Transition governance state & version | JSON: `governance_state`, `version_label` | `200 OK` / `400` / `404` |
| `POST` | `/api/v1/documents/{id}/reprocess` | Documents | Trigger background reprocessing | `id` path param | `200 OK` / `404` |
| `DELETE` | `/api/v1/documents/{id}` | Documents | Delete document, vectors & cascade dependencies | `id` path param | `200 OK` / `404` |
| `POST` | `/api/v1/projects/{id}/ask` | AI Assistant | Grounded RAG Q&A with claim verification | JSON: `query`, `document_ids`, `version_label`, `strategy`, `top_k` | `200 OK` / `404` |
| `POST` | `/api/v1/sessions/{s_id}/messages/{m_id}/review` | Human Review | Submit formal engineer review & sign-off | JSON: `decision`, `reviewer_id`, `feedback`, `corrected_facts` | `200 OK` / `400` / `404` |
| `GET` | `/api/v1/projects/{id}/reviews` | Audit Log | Retrieve query review sign-off history | `id` path param | `200 OK` |
| `GET` | `/api/v1/projects/{id}/entities` | Entities | List extracted architecture entities | `id` path param, `version_label` filter | `200 OK` |
| `GET` | `/api/v1/projects/{id}/ports_and_signals` | Entities | Dedicated AUTOSAR Ports & Signals list | `component`, `direction`, `version_label` filters | `200 OK` |
| `GET` | `/api/v1/projects/{id}/topology` | Topology | Generate Mermaid diagram & directed edges | `id` path param | `200 OK` |
| `GET` | `/api/v1/projects/{id}/impact` | Change Impact | BFS downstream dependency impact traversal | `root_entity_name` query param | `200 OK` |
| `POST` | `/api/v1/entities/{id}/review` | Entities | Update entity review status | JSON: `status` (confirmed, rejected, pending) | `200 OK` / `404` |
| `GET` | `/api/v1/projects/{id}/comparisons` | Comparisons | List saved revision comparison runs | `id` path param | `200 OK` |
| `POST` | `/api/v1/projects/{id}/comparisons` | Comparisons | Run diff & deterministic rename detection | JSON: `baseline_document_id`, `comparison_document_id` | `200 OK` / `400` |
| `GET` | `/api/v1/projects/{id}/findings` | Findings | List architectural rule violation findings | `id` path param | `200 OK` |
| `PATCH` | `/api/v1/findings/{id}` | Findings | Update finding review status & notes | JSON: `review_status`, `reviewer_comments` | `200 OK` / `404` |
| `GET` | `/api/v1/projects/{id}/reports` | Reports | List generated reports with disk validation | `id` path param | `200 OK` |
| `POST` | `/api/v1/projects/{id}/reports` | Reports | Generate report (PDF, MD, CSV, JSON) | JSON: `report_type`, `format`, `component_name` | `200 OK` / `400` |
| `GET` | `/api/v1/reports/{id}/download` | Reports | Download generated report artifact | `id` path param | `200 OK` / `404` / `422` |
| `GET` | `/api/v1/settings` | Settings | Get extraction & enterprise rule parameters | None | `200 OK` |
| `POST` | `/api/v1/settings` | Settings | Update extraction parameters & rules | JSON: `chunk_size`, `chunk_overlap`, rules | `200 OK` / `400` |
| `GET` | `/api/v1/settings/system` | Settings | Safe system configuration (no secrets) | None | `200 OK` |
| `GET` | `/api/v1/diagnostics` | Diagnostics | Probe 6 core subsystems with latency stats | None | `200 OK` |
| `GET` | `/api/v1/projects/{id}/evaluation/dataset` | Evaluation | Benchmark dataset provenance & query counts | `id` path param | `200 OK` |
| `POST` | `/api/v1/projects/{id}/evaluation/run` | Evaluation | Execute benchmark (MRR, Hit@1, Latency) | JSON: `strategy`, `top_k`, `max_queries` | `200 OK` |
| `GET` | `/api/v1/projects/{id}/evaluation/history` | Evaluation | List historical benchmark runs | `id` path param | `200 OK` |

---

## 3. Representative JSON Schemas

### 3.1 Grounded Query Request & Response
**Request** (`POST /api/v1/projects/1/ask`):
```json
{
  "query": "What software components are defined in the Powertrain architecture?",
  "document_ids": [],
  "version_label": "All Versions",
  "strategy": "hybrid",
  "top_k": 5
}
```

**Response** (`200 OK`):
```json
{
  "message_id": 4,
  "session_id": 2,
  "answer": "According to the AUTOSAR_Adaptive_Powertrain_HLD.pdf document (Page 1-1, v1.0) [AUTOSAR ADAPTIVE PLATFORM SPECIFICATION], the following software components (SWCs) are defined in the Powertrain architecture:\n\n* PowertrainManager_SWC: The master supervisory controller executing vehicle operating mode management...\n* TorqueArbitration_SWC: The core arbitration unit responsible for merging torque demands...\n* BatterySafety_SWC: High-voltage battery supervisor monitoring pack voltage...\n* InverterActuator_SWC: Low-level hardware abstraction component...",
  "citations": [
    {
      "citation_id": 1,
      "document_id": 2,
      "document_name": "AUTOSAR_Adaptive_Powertrain_HLD.pdf",
      "version_label": "1.0",
      "section_heading": "AUTOSAR ADAPTIVE PLATFORM SPECIFICATION",
      "page_start": 1,
      "page_end": 1,
      "content": "AUTOSAR ADAPTIVE PLATFORM SPECIFICATION\nDocument ID: HLD-AUTOSAR-PWR-2026..."
    }
  ],
  "claims": [
    {
      "claim_id": 1,
      "claim_text": "PowertrainManager_SWC executes vehicle operating mode management.",
      "status": "Grounded",
      "verification_reason": "Verified against retrieved evidence from AUTOSAR_Adaptive_Powertrain_HLD.pdf (Page 1-1)."
    }
  ],
  "grounding_score": 100.0,
  "confidence_level": "HIGH",
  "review_recommendation": "STANDARD REVIEW",
  "strategy": "hybrid",
  "top_k": 5,
  "latencies": {
    "dense_latency_ms": 28.5,
    "bm25_latency_ms": 2.1,
    "fusion_latency_ms": 0.4,
    "llm_latency_ms": 3410.2,
    "total_latency_ms": 3441.2
  }
}
```

### 3.2 Safe System Configuration Response
**Response** (`GET /api/v1/settings/system`):
```json
{
  "app_name": "AUTOSAR AI",
  "app_env": "development",
  "llm_provider": "ollama",
  "llm_model": "llama3.2:3b",
  "llm_base_url": "http://localhost:11434",
  "has_api_key": false,
  "embedding_model": "all-MiniLM-L6-v2",
  "vector_store_dir": "./data/vector_store",
  "upload_dir": "./data/uploads",
  "export_dir": "./data/exports",
  "max_upload_mb": 50,
  "is_local_inference": true
}
```

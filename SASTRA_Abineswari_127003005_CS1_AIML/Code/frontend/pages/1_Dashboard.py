import streamlit as st
import os
import sys
import requests

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header, get_active_engine_info

st.set_page_config(page_title="Dashboard — AUTOSAR AI", page_icon="📊", layout="wide")
inject_custom_css()

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

engine_info = get_active_engine_info(api_base)
status_badge = "badge-success" if engine_info.get("overall_status") == "PASS" else ("badge-error" if engine_info.get("overall_status") == "FAIL" else "badge-pending")
status_label = f"System: {engine_info.get('overall_status', 'UNKNOWN')}"

render_header(
    title="Engineering Dashboard",
    subtitle="AUTOSAR High-Level Design Intelligence, Subsystem Telemetry & Asset Status",
    badge_text=status_label,
    badge_type=status_badge
)

# Fetch project metrics from backend
metrics = {
    "total_documents": 0, 
    "processed_documents": 0, 
    "total_chunks": 0,
    "total_entities": 0, 
    "total_ports": 0,
    "total_signals": 0,
    "total_relationships": 0,
    "open_findings": 0
}
try:
    res = requests.get(f"{api_base}/projects/{project_id}/metrics", timeout=3)
    if res.status_code == 200:
        metrics.update(res.json())
except Exception:
    pass

# Row 1: High-level document and architectural metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Processed Specifications", f"{metrics['processed_documents']} / {metrics['total_documents']}")
m2.metric("Indexed Chunks", str(metrics.get("total_chunks", 0)))
m3.metric("Architectural Entities", str(metrics["total_entities"]))
m4.metric("Open Rule Findings", str(metrics["open_findings"]))

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# Row 2: Secondary architectural telemetry with dynamic active engine
sm1, sm2, sm3, sm4 = st.columns(4)
sm1.metric("Extracted Ports", str(metrics.get("total_ports", 0)))
sm2.metric("Extracted Signals", str(metrics.get("total_signals", 0)))
sm3.metric("Dependency Edges", str(metrics.get("total_relationships", 0)))
engine_display = f"{engine_info.get('provider', 'ollama').capitalize()} ({engine_info.get('model', 'llama3.2:3b')})"
sm4.metric("Active LLM Engine", engine_display)

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

col_act, col_sys = st.columns([2, 1])

with col_act:
    with st.container(border=True):
        st.subheader("Specification Repository")
        st.caption("Active AUTOSAR design documents ingested for architectural analysis:")
        
        docs = []
        try:
            res = requests.get(f"{api_base}/projects/{project_id}/documents", timeout=3)
            if res.status_code == 200:
                docs = res.json()
        except Exception:
            pass
        
        if docs:
            table_html = """<table class="sa-table">
                <tr>
                    <th>Specification Document</th>
                    <th>Version</th>
                    <th>Governance</th>
                    <th>Processing Status</th>
                    <th>Pages</th>
                </tr>"""
            for d in docs:
                status_class = "badge-success" if d['status'] == 'READY' else ("badge-processing" if d['status'] == 'PROCESSING' else ("badge-error" if d['status'] == 'FAILED' else "badge-pending"))
                gov_lbl = d.get('governance_state', 'DRAFT')
                gov_class = "badge-navy" if gov_lbl == "APPROVED" else ("badge-pending" if gov_lbl == "IN_REVIEW" else "badge-neutral")
                ver_val = d.get('version_label', '1.0') or '1.0'
                pg_count = d.get('page_count') or '-'
                table_html += f"""
                <tr>
                    <td style="font-weight: 600; color: #0F172A;">📄 {d['original_filename']}</td>
                    <td><code>v{ver_val}</code></td>
                    <td><span class="badge {gov_class}">{gov_lbl}</span></td>
                    <td><span class="badge {status_class}">{d['status']}</span></td>
                    <td>{pg_count}</td>
                </tr>"""
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("No documents uploaded yet. Navigate to Documents to upload your first AUTOSAR specification.")

with col_sys:
    with st.container(border=True):
        st.subheader("Subsystem Diagnostics")
        st.caption("Live health across core services:")
        
        # Load diagnostics
        diag_data = None
        try:
            d_res = requests.get(f"{api_base}/diagnostics", timeout=5)
            if d_res.status_code == 200:
                diag_data = d_res.json()
        except Exception:
            pass

        if diag_data:
            subsystems = diag_data.get("subsystems", {})
            for key, sub in subsystems.items():
                s_stat = sub.get("status", "UNKNOWN")
                badge = "badge-success" if s_stat == "PASS" else ("badge-error" if s_stat == "FAIL" else "badge-pending")
                svc_title = sub.get('service', key.replace('_', ' ').title())
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; padding: 6px 0; border-bottom: 1px solid #F1F5F9; font-size:0.87rem;'>
                    <span style='color:#334155; font-weight:500;'>{svc_title}</span>
                    <span class='badge {badge}'>{s_stat}</span>
                </div>
                """, unsafe_allow_html=True)
            
            p_info = diag_data.get("active_provider_info", {})
            mode_label = "Local Offline" if p_info.get("is_local", True) else "Cloud Hosted"
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            st.caption(f"Provider: **{p_info.get('provider', 'ollama').upper()}** ({p_info.get('model', 'llama3.2:3b')}) • **{mode_label}**")
        else:
            st.warning("Diagnostics check is running or API is temporarily busy.")

        if st.button("🔄 Refresh Subsystem Diagnostics", use_container_width=True):
            st.rerun()

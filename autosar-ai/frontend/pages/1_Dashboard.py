import streamlit as st
import os
import sys

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Dashboard - AUTOSAR AI", page_icon="📊", layout="wide")
inject_custom_css()

import requests

render_header("Overview", "Project Analytics & Status")

# Fetch metrics
project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

metrics = {"total_documents": 0, "processed_documents": 0, "total_entities": 0, "open_findings": 0}
try:
    res = requests.get(f"{api_base}/projects/{project_id}/metrics")
    if res.status_code == 200:
        metrics = res.json()
except Exception:
    pass

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Documents", str(metrics["total_documents"]))
m2.metric("Processed Documents", str(metrics["processed_documents"]))
m3.metric("Architecture Entities", str(metrics["total_entities"]))
m4.metric("Open Findings", str(metrics["open_findings"]))

st.markdown("<br>", unsafe_allow_html=True)

col_act, col_sys = st.columns([2, 1])

with col_act:
    with st.container(border=True):
        st.subheader("Recent Documents")
        
        # Fetch recent docs
        docs = []
        try:
            res = requests.get(f"{api_base}/projects/{project_id}/documents")
            if res.status_code == 200:
                docs = res.json()
        except Exception:
            pass
        
        if docs:
            table_html = """<table style="width: 100%; text-align: left; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #E5E7EB; color: #6B7280; font-size: 0.9rem;">
                    <th style="padding: 10px 0;">Document Name</th>
                    <th style="padding: 10px 0;">Status</th>
                </tr>"""
            for d in docs[:5]: # recent 5
                status_class = "badge-success" if d['status'] == 'READY' else ("badge-processing" if d['status'] == 'PROCESSING' else "badge-pending")
                table_html += f"""
                <tr style="border-bottom: 1px solid #F3F4F6; font-size: 0.95rem;">
                    <td style="padding: 12px 0; color: #111827; font-weight: 500;">{d['original_filename']}</td>
                    <td style="padding: 12px 0;"><span class="{status_class}">{d['status']}</span></td>
                </tr>"""
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("No documents uploaded yet. Use the Quick Actions to upload one.")

with col_sys:
    with st.container(border=True):
        st.subheader("System Subsystems")
        
        if st.button("Run Full Diagnostics", use_container_width=True):
            with st.spinner("Executing runtime checks..."):
                diag_data = None
                try:
                    res = requests.get(f"{api_base}/diagnostics", timeout=15)
                    if res.status_code == 200:
                        diag_data = res.json()
                except Exception as e:
                    st.error(f"Diagnostics connection error: {str(e)}")
                
                if diag_data:
                    subsystems = diag_data.get("subsystems", {})
                    for key, sub in subsystems.items():
                        badge = "badge-success" if sub["status"] == "PASS" else ("badge-error" if sub["status"] == "FAIL" else "badge-pending")
                        st.markdown(f"""
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:0.9rem;'>
                            <span style='color:#374151; font-weight:500;'>{sub.get('service', key)}</span>
                            <span class='{badge}'>{sub['status']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    llm_info = diag_data.get("active_provider_info", {})
                    st.caption(f"Active Provider: **{llm_info.get('provider')}** | Model: **{llm_info.get('model')}**")
                else:
                    st.markdown("<p style='color: #DC2626; font-size: 0.95rem;'>API Backend is unreachable at http://127.0.0.1:8000</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #6B7280; margin-bottom: 12px; font-size: 0.95rem;'>Click 'Run Full Diagnostics' to verify Ollama, Database, Vector Store, and PyMuPDF.</p>", unsafe_allow_html=True)
            st.caption("Default Model: llama3.2:3b (Local Ollama)")

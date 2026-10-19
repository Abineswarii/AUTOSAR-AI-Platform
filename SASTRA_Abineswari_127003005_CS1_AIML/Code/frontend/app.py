import streamlit as st
import os
import sys
import requests

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from frontend.utils.ui import inject_custom_css, render_header, get_active_engine_info

st.set_page_config(
    page_title="AUTOSAR AI — Engineering Intelligence Platform",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

api_base = "http://127.0.0.1:8000/api/v1"
engine_info = get_active_engine_info(api_base)
status_badge = "badge-success" if engine_info.get("reachable") else "badge-error"
status_text = f"LLM: {engine_info.get('model', 'offline')}"

render_header(
    title="AUTOSAR AI",
    subtitle="High-Level Design Document Intelligence & Architecture Governance Platform",
    badge_text=status_text,
    badge_type=status_badge
)

# Fetch quick metrics for the welcome hero
metrics = {"total_documents": 0, "processed_documents": 0, "total_entities": 0, "open_findings": 0}
try:
    res = requests.get(f"{api_base}/projects/1/metrics", timeout=2)
    if res.status_code == 200:
        metrics.update(res.json())
except Exception:
    pass

# Metric Hero Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Indexed Specifications", f"{metrics['processed_documents']} / {metrics['total_documents']}")
m2.metric("Extracted Entities", str(metrics['total_entities']))
m3.metric("Compliance Findings", str(metrics['open_findings']))
m4.metric("Active LLM Engine", f"{engine_info.get('provider', 'ollama').capitalize()} ({engine_info.get('model', 'llama3.2:3b')})")

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# Main Two-Column Layout
col_main, col_nav = st.columns([2.1, 1])

with col_main:
    with st.container(border=True):
        st.subheader("Platform Architecture & Operational Scope")
        st.markdown("""
        **AUTOSAR AI** is an automotive systems engineering workbench designed for rigorous analysis of 
        AUTOSAR Classic and Adaptive Platform High-Level Design (HLD) specifications, Interface Control 
        Documents (ICDs), and System Requirement Specifications (SRS).
        """)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            #### 🔍 Grounded RAG & Retrieval
            - **Hybrid Retrieval**: Combines dense semantic embeddings (`all-MiniLM-L6-v2`) with sparse lexical matching (BM25) via Reciprocal Rank Fusion ($k=60$).
            - **Claim Traceability**: Decomposes model responses into discrete technical claims, cross-verifying each against explicit source citations.
            - **Truthful Abstention**: Formulated to abstain when evidence is insufficient, preventing synthetic hallucination.
            """)
        with c2:
            st.markdown("""
            #### 🧩 Architecture Governance
            - **Entity Inventory**: Automatically parses Software Components (SWC), Runnables, Ports (PPort/RPort), and Signals.
            - **Topology Graphs**: Constructs directed dependency diagrams and performs BFS traversal for change-impact analysis.
            - **Rule Validation**: Flags unmanaged IPC memory access, missing array bounds, circular loops, and type mismatches.
            """)

with col_nav:
    with st.container(border=True):
        st.subheader("Workspace Navigation")
        st.caption("Select a workflow to begin document analysis:")

        if st.button("📄 Document Management", use_container_width=True):
            st.switch_page("pages/2_Documents.py")

        if st.button("🤖 AI Engineering Assistant", use_container_width=True):
            st.switch_page("pages/4_AI_Assistant.py")

        if st.button("🧩 Architecture Explorer", use_container_width=True):
            st.switch_page("pages/3_Architecture_Explorer.py")

        if st.button("⚖️ Document Version Comparison", use_container_width=True):
            st.switch_page("pages/5_Comparisons.py")

        if st.button("⚠️ Findings & Audit Reviews", use_container_width=True):
            st.switch_page("pages/6_Findings.py")

        if st.button("📥 Reports & Artifacts", use_container_width=True):
            st.switch_page("pages/7_Reports.py")

        if st.button("⚙️ System Status & Settings", use_container_width=True):
            st.switch_page("pages/8_Settings.py")

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #64748B;'>
    <span>AUTOSAR AI Platform • Version 1.0.0</span>
    <span>Engineered for Automotive Software Quality & ISO 26262 Design Traceability</span>
</div>
""", unsafe_allow_html=True)

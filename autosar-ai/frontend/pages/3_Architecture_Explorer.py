import streamlit as st
import os
import sys

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Architecture Explorer", page_icon="🧩", layout="wide")
inject_custom_css()

import requests

render_header("Architecture Explorer", "Component inventory and dependencies")

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

with st.container(border=True):
    col_filter1, col_filter2 = st.columns([1, 3])
    with col_filter1:
        type_filter = st.selectbox("Entity Type", ["All", "Software Component", "Runnable", "Interface"])
    with col_filter2:
        search_q = st.text_input("Search Components", placeholder="e.g. EngineControlUnit")

entities = []
try:
    res = requests.get(f"{api_base}/projects/{project_id}/entities")
    if res.status_code == 200:
        entities = res.json()
except Exception:
    pass

if type_filter != "All":
    entities = [e for e in entities if (e.get("entity_type") or e.get("type")) == type_filter]
if search_q:
    entities = [e for e in entities if search_q.lower() in e.get("name", "").lower()]

# Fetch relationships
rels = []
try:
    rel_res = requests.get(f"{api_base}/projects/{project_id}/relationships")
    if rel_res.status_code == 200:
        rels = rel_res.json()
except Exception:
    pass

if entities:
    for e in entities:
        etype = e.get("entity_type") or e.get("type", "Component")
        r_status = e.get("review_status", "pending")
        status_badge = "badge-success" if r_status == 'confirmed' else ("badge-error" if r_status == 'rejected' else "badge-pending")
        with st.expander(f"🧩 [{etype}] {e.get('name', 'Unknown')}  —  {r_status.upper()}", expanded=False):
            info_c1, info_c2 = st.columns(2)
            with info_c1:
                st.write(f"**Entity Type:** {etype}")
                st.write(f"**Name:** `{e.get('name')}`")
                st.write(f"**Confidence:** {round(e.get('confidence', 0.9) * 100)}%")
                st.write(f"**Source Page:** Page {e.get('source_page') or 'N/A'}")
            with info_c2:
                st.write(f"**Status:** <span class='{status_badge}'>{r_status}</span>", unsafe_allow_html=True)
                st.write(f"**Extraction Method:** {e.get('extraction_method', 'regex_heuristic')}")
                
            if e.get("source_excerpt"):
                st.markdown("**Source Excerpt:**")
                st.code(e["source_excerpt"], language="text")
                
            # Entity Review Actions
            st.markdown("**Review Verification:**")
            rev_c1, rev_c2, rev_c3 = st.columns(3)
            with rev_c1:
                if st.button("✅ Confirm", key=f"conf_{e['id']}", use_container_width=True):
                    requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "confirmed"})
                    st.success("Marked as Confirmed!")
                    st.rerun()
            with rev_c2:
                if st.button("❌ Reject", key=f"rej_{e['id']}", use_container_width=True):
                    requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "rejected"})
                    st.warning("Marked as Rejected.")
                    st.rerun()
            with rev_c3:
                if st.button("⏳ Reset Pending", key=f"rst_{e['id']}", use_container_width=True):
                    requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "pending"})
                    st.info("Reset to Pending.")
                    st.rerun()
else:
    st.info("No architectural entities found matching current filters. Upload a specification PDF to extract entities.")

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Document Comparison", page_icon="⚖️", layout="wide")
inject_custom_css()

import requests
import json

render_header("Document Comparison", "Compare baseline and modified architectural documents")

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

# Fetch documents for selection
docs = []
try:
    res = requests.get(f"{api_base}/projects/{project_id}/documents")
    if res.status_code == 200:
        docs = res.json()
except Exception:
    pass
    
doc_options = {d["original_filename"]: d["id"] for d in docs if d["status"] == "READY"}

tab_compare, tab_history = st.tabs(["Document Comparison", "Comparison History"])

with tab_compare:
    with st.container(border=True):
        st.subheader("Run Document Comparison")
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        base_doc_name = st.selectbox("Baseline Document", list(doc_options.keys()) if doc_options else ["No processed docs available"], key="sel_base")
    with c2:
        comp_doc_name = st.selectbox("Comparison Document", list(doc_options.keys()) if doc_options else ["No processed docs available"], key="sel_comp")
    with c3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        can_run = bool(doc_options and len(doc_options) >= 2)
        if st.button("Compare Documents", use_container_width=True, disabled=not can_run):
            if base_doc_name == comp_doc_name:
                st.error("Cannot compare a document to itself. Please choose two distinct documents.")
            else:
                with st.spinner("Analyzing architectural differences..."):
                    payload = {
                        "baseline_document_id": doc_options[base_doc_name],
                        "comparison_document_id": doc_options[comp_doc_name]
                    }
                    res = requests.post(f"{api_base}/projects/{project_id}/comparisons", json=payload)
                    if res.status_code == 200:
                        comp_data = res.json()
                        st.session_state.current_comparison = comp_data
                        st.success("Comparison completed successfully!")
                    else:
                        st.error(f"Comparison failed: {res.text}")
    st.markdown("</div>", unsafe_allow_html=True)

    if "current_comparison" in st.session_state:
        comp_data = st.session_state.current_comparison
        try:
            results = json.loads(comp_data.get("results_json", "{}"))
        except:
            results = {"added": [], "removed": [], "modified": []}
            
        added_list = results.get("added", [])
        removed_list = results.get("removed", [])
        modified_list = results.get("modified", [])

        st.markdown("### Comparison Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Added Entities", len(added_list))
        m2.metric("Removed Entities", len(removed_list))
        m3.metric("Modified Entities", len(modified_list))

        if not added_list and not removed_list and not modified_list:
            st.info("No architectural differences detected between the selected specifications.")
        else:
            if added_list:
                st.markdown("#### ➕ Added Components")
                for item in added_list:
                    st.markdown(f"- **[{item['type']}]** `{item['name']}` (Page {item.get('source_page', 1)}) — *{item.get('description', '')}*")
            
            if removed_list:
                st.markdown("#### ➖ Removed Components")
                for item in removed_list:
                    st.markdown(f"- **[{item['type']}]** `{item['name']}` (Page {item.get('source_page', 1)}) — *{item.get('description', '')}*")
                    
            if modified_list:
                st.markdown("#### 🔄 Modified Components")
                for item in modified_list:
                    with st.expander(f"[{item['type']}] {item['name']}"):
                        st.write(f"**Baseline Excerpt (Page {item.get('baseline_page', 1)}):**")
                        st.code(item.get('baseline_excerpt', ''), language='text')
                        st.write(f"**Comparison Excerpt (Page {item.get('comparison_page', 1)}):**")
                        st.code(item.get('comparison_excerpt', ''), language='text')

with tab_history:
    with st.container(border=True):
        st.subheader("Saved Comparison Runs")
        
        past_comps = []
        try:
            hist_res = requests.get(f"{api_base}/projects/{project_id}/comparisons")
            if hist_res.status_code == 200:
                past_comps = hist_res.json()
        except Exception as e:
            st.error(f"Failed to fetch history: {str(e)}")
            
        if past_comps:
            for pc in past_comps:
                with st.expander(f"⚖️ Baseline: {pc.get('baseline_document_name')} vs {pc.get('comparison_document_name')} — {pc.get('created_at', '')[:19]}", expanded=False):
                    st.write(f"**Added:** {pc.get('added_count', 0)} | **Removed:** {pc.get('removed_count', 0)} | **Modified:** {pc.get('modified_count', 0)}")
                    if st.button("Load This Result", key=f"load_comp_{pc['id']}"):
                        st.session_state.current_comparison = pc
                        st.success("Loaded into Comparison view!")
                        st.rerun()
        else:
            st.info("No comparison history saved yet.")

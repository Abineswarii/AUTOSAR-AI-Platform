import streamlit as st
import os
import sys

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Documents - AUTOSAR AI", page_icon="📄", layout="wide")
inject_custom_css()

import requests

render_header("Documents", "Manage your specifications and design documents")

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

col1, col2 = st.columns([3, 1])

with col1:
    with st.container(border=True):
        st.subheader("Document Repository")
        
        # Filters
        f1, f2, f3 = st.columns(3)
        f1.selectbox("Project", ["Default Project"], disabled=True)
        status_filter = f2.selectbox("Status", ["All", "READY", "PROCESSING", "FAILED", "UPLOADED"])
        search_q = f3.text_input("Search", placeholder="Search documents...")
        
        docs = []
        try:
            res = requests.get(f"{api_base}/projects/{project_id}/documents")
            if res.status_code == 200:
                docs = res.json()
        except Exception:
            pass
            
        if status_filter != "All":
            docs = [d for d in docs if d.get("status") == status_filter]
        if search_q:
            docs = [d for d in docs if search_q.lower() in d.get("original_filename", "").lower()]
        
        if docs:
            for d in docs:
                status_label = d.get('status', 'UNKNOWN')
                doc_name = d.get('original_filename', f"Document #{d.get('id')}")
                with st.expander(f"📄 {doc_name}  [{status_label}]", expanded=False):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Document ID:** {d.get('id')}")
                        st.write(f"**Pages:** {d.get('page_count') or 'N/A'}")
                        st.write(f"**Status:** {status_label}")
                    with col_info2:
                        sha_val = d.get('sha256_hash') or 'N/A'
                        sha_display = f"{sha_val[:16]}..." if len(sha_val) > 16 else sha_val
                        st.write(f"**SHA256:** `{sha_display}`")
                        if d.get("error_message"):
                            st.error(f"Error: {d['error_message']}")
                            
                    act_col1, act_col2 = st.columns([1, 1])
                    with act_col1:
                        if st.button("🔄 Reprocess", key=f"reprocess_{d.get('id')}", use_container_width=True):
                            try:
                                rep_res = requests.post(f"{api_base}/documents/{d.get('id')}/reprocess")
                                if rep_res.status_code == 200:
                                    st.success(f"Reprocessing started for {doc_name}!")
                                    st.rerun()
                                else:
                                    st.error("Reprocess request failed.")
                            except Exception as e:
                                st.error(str(e))
                                
                    with act_col2:
                        if st.button("🗑️ Delete", key=f"del_{d.get('id')}", use_container_width=True):
                            try:
                                del_res = requests.delete(f"{api_base}/documents/{d.get('id')}")
                                if del_res.status_code == 200:
                                    st.success(f"Deleted {doc_name}")
                                    st.rerun()
                                else:
                                    st.error("Delete request failed.")
                            except Exception as e:
                                st.error(str(e))
        else:
            st.info("No documents found matching the filter.")

with col2:
    with st.container(border=True):
        st.subheader("Upload Document")
        st.caption("Drag and drop an AUTOSAR specification or HLD PDF file here.")
        uploaded_file = st.file_uploader("Select PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Upload & Process", use_container_width=True):
                with st.spinner("Uploading and analyzing document..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        res = requests.post(f"{api_base}/projects/{project_id}/documents", files=files)
                        if res.status_code == 200:
                            st.success("Uploaded successfully! It is now processing.")
                            st.rerun()
                        else:
                            st.error(f"Failed to upload: {res.text}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

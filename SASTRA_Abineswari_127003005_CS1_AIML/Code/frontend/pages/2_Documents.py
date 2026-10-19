import streamlit as st
import os
import sys
import requests

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header, render_empty_state

st.set_page_config(page_title="Document Management — AUTOSAR AI", page_icon="📄", layout="wide")
inject_custom_css()

render_header(
    title="Document Management",
    subtitle="Ingest AUTOSAR specifications, manage revisions & configure lifecycle governance",
    badge_text="Repository Active",
    badge_type="badge-navy"
)

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

col1, col2 = st.columns([2.2, 1])

with col1:
    with st.container(border=True):
        st.subheader("Specification Repository")
        
        # Filters
        f1, f2, f3, f4 = st.columns([1, 1.2, 1.2, 1.6])
        f1.selectbox("Project", ["Default Project"], disabled=True)
        status_filter = f2.selectbox("Processing Status", ["All", "READY", "PROCESSING", "FAILED", "UPLOADED"])
        gov_filter = f3.selectbox("Governance State", ["All", "DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED"])
        search_q = f4.text_input("Search Specifications", placeholder="Filter by filename...")
        
        docs = []
        try:
            res = requests.get(f"{api_base}/projects/{project_id}/documents", timeout=5)
            if res.status_code == 200:
                docs = res.json()
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend server on http://127.0.0.1:8000.")
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
            
        if status_filter != "All":
            docs = [d for d in docs if d.get("status") == status_filter]
        if gov_filter != "All":
            docs = [d for d in docs if d.get("governance_state") == gov_filter]
        if search_q.strip():
            docs = [d for d in docs if search_q.strip().lower() in d.get("original_filename", "").lower()]
        
        if docs:
            st.caption(f"Displaying {len(docs)} specification document(s):")
            for d in docs:
                status_label = d.get('status', 'UNKNOWN')
                gov_label = d.get('governance_state', 'DRAFT')
                ver_label = d.get('version_label', '1.0') or '1.0'
                doc_name = d.get('original_filename', f"Document #{d.get('id')}")
                
                status_class = "badge-success" if status_label == 'READY' else ("badge-processing" if status_label == 'PROCESSING' else ("badge-error" if status_label == 'FAILED' else "badge-pending"))
                gov_class = "badge-navy" if gov_label == "APPROVED" else ("badge-pending" if gov_label == "IN_REVIEW" else ("badge-error" if gov_label == "SUPERSEDED" else "badge-neutral"))
                
                with st.expander(f"📄 {doc_name}  —  v{ver_label}  [{gov_label}]  [{status_label}]", expanded=False):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"**Document ID:** `{d.get('id')}`")
                        st.markdown(f"**Version Label:** `v{ver_label}`")
                        st.markdown(f"**Governance State:** <span class='badge {gov_class}'>{gov_label}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Processing Status:** <span class='badge {status_class}'>{status_label}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Extracted Pages:** {d.get('page_count') or 'N/A'}")
                    with col_info2:
                        sha_val = d.get('sha256_hash') or 'N/A'
                        sha_display = f"{sha_val[:16]}..." if len(sha_val) > 16 else sha_val
                        st.markdown(f"**SHA-256 Digest:** `{sha_display}`")
                        st.markdown(f"**Created At:** {d.get('created_at', 'N/A')}")
                        if d.get("error_message"):
                            st.error(f"Processing Error: {d['error_message']}")

                    # Governance update form
                    st.markdown("---")
                    st.caption("⚙️ **Lifecycle Governance Transition**")
                    gov_col1, gov_col2, gov_col3 = st.columns([2, 1.2, 1.2])
                    with gov_col1:
                        new_gov = st.selectbox(
                            "Target Governance State", 
                            ["DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED"],
                            index=["DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED"].index(gov_label) if gov_label in ["DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED"] else 0,
                            key=f"gov_sel_{d.get('id')}"
                        )
                    with gov_col2:
                        new_ver = st.text_input("Specification Version", value=ver_label, key=f"ver_input_{d.get('id')}")
                    with gov_col3:
                        st.write("")
                        st.write("")
                        if st.button("Apply State", key=f"btn_gov_{d.get('id')}", use_container_width=True):
                            try:
                                patch_res = requests.patch(
                                    f"{api_base}/documents/{d.get('id')}/governance",
                                    json={"governance_state": new_gov, "version_label": new_ver}
                                )
                                if patch_res.status_code == 200:
                                    st.success(f"Updated governance state to {new_gov} (v{new_ver})")
                                    st.rerun()
                                else:
                                    st.error(f"Update failed: {patch_res.text}")
                            except Exception as e:
                                st.error(str(e))
                            
                    act_col1, act_col2 = st.columns([1, 1])
                    with act_col1:
                        if st.button("🔄 Reprocess Document", key=f"reprocess_{d.get('id')}", use_container_width=True):
                            try:
                                rep_res = requests.post(f"{api_base}/documents/{d.get('id')}/reprocess")
                                if rep_res.status_code == 200:
                                    st.success(f"Reprocessing initiated for {doc_name}")
                                    st.rerun()
                                else:
                                    st.error("Reprocess request failed.")
                            except Exception as e:
                                st.error(str(e))
                                
                    with act_col2:
                        if st.button("🗑️ Delete Specification", key=f"del_{d.get('id')}", use_container_width=True):
                            try:
                                del_res = requests.delete(f"{api_base}/documents/{d.get('id')}")
                                if del_res.status_code == 200:
                                    st.success(f"Deleted {doc_name} and associated vector embeddings")
                                    st.rerun()
                                else:
                                    st.error("Delete request failed.")
                            except Exception as e:
                                st.error(str(e))
        else:
            render_empty_state(
                icon="📄",
                title="No Matching Specifications",
                description="Upload an AUTOSAR High-Level Design (HLD) or System Specification PDF using the panel on the right."
            )

with col2:
    with st.container(border=True):
        st.subheader("Upload Specification")
        st.caption("Upload an AUTOSAR design document for automated extraction, indexing & validation:")
        
        uploaded_file = st.file_uploader("Select Specification PDF", type=["pdf"])
        upload_ver = st.text_input("Specification Version", value="1.0", placeholder="e.g. 1.0, 2.0")
        upload_gov = st.selectbox("Governance State", ["DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED"], index=0)
        
        if uploaded_file is not None:
            # Client-side empty file guard
            if uploaded_file.size == 0:
                st.error("The selected file is empty (0 bytes). Please select a valid PDF.")
            else:
                st.caption(f"Selected: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 1)} KB)")
                if st.button("Upload & Process Document", use_container_width=True):
                    with st.spinner("Uploading and analyzing document..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                            data = {
                                "version_label": upload_ver.strip() if upload_ver else "1.0",
                                "governance_state": upload_gov
                            }
                            res = requests.post(f"{api_base}/projects/{project_id}/documents", files=files, data=data)
                            if res.status_code == 200:
                                st.success("Uploaded successfully! Document ingested and queued for indexing.")
                                st.rerun()
                            else:
                                st.error(f"Upload failed ({res.status_code}): {res.text}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")

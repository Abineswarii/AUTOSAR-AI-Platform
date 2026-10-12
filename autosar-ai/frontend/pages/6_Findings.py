import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Findings & Validation", page_icon="✅", layout="wide")
inject_custom_css()

render_header("Findings & Validation", "Architectural issues and rule validation")

import requests
import json

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

with st.container(border=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        severity_filter = st.selectbox("Severity", ["All", "High", "Medium", "Low"])
    with f2:
        status_filter = st.selectbox("Status", ["All", "open", "confirmed", "resolved", "rejected"])
    with f3:
        search_q = st.text_input("Search Findings", placeholder="Search descriptions...")

findings = []
try:
    res = requests.get(f"{api_base}/projects/{project_id}/findings")
    if res.status_code == 200:
        findings = res.json()
except Exception as e:
    st.error(f"Failed to fetch findings: {str(e)}")

# Apply filters
if severity_filter != "All":
    findings = [f for f in findings if (f.get("severity") or "").lower() == severity_filter.lower()]
if status_filter != "All":
    findings = [f for f in findings if (f.get("review_status") or "").lower() == status_filter.lower()]
if search_q:
    findings = [f for f in findings if search_q.lower() in (f.get("description") or "").lower()]

if findings:
    st.markdown(f"**Found {len(findings)} architectural finding(s):**")
    for f in findings:
        sev = f.get("severity", "Low")
        sev_color = "#DC2626" if sev == "High" else ("#D97706" if sev == "Medium" else "#2563EB")
        status_badge = "badge-success" if f.get("review_status") == "confirmed" else ("badge-processing" if f.get("review_status") == "resolved" else "badge-pending")
        
        with st.expander(f"⚠️ [{sev}] {f.get('finding_type', 'Rule Violation')} — {f.get('description', '')[:70]}...", expanded=False):
            fc1, fc2 = st.columns(2)
            with fc1:
                st.write(f"**Finding ID:** {f['id']}")
                st.write(f"**Severity:** <span style='color:{sev_color}; font-weight:600;'>{sev}</span>", unsafe_allow_html=True)
                st.write(f"**Type:** {f.get('finding_type')}")
            with fc2:
                st.write(f"**Status:** <span class='{status_badge}'>{f.get('review_status')}</span>", unsafe_allow_html=True)
                st.write(f"**Document ID:** {f.get('document_id') or 'N/A'}")
                
            st.markdown(f"**Description:** {f.get('description')}")
            
            if f.get("evidence_json"):
                st.markdown("**Evidence / Trace Context:**")
                st.code(f["evidence_json"], language="json")
                
            st.markdown("---")
            st.markdown("**Review & Workflow Actions:**")
            rc1, rc2 = st.columns([1, 2])
            with rc1:
                new_status = st.selectbox(
                    "Update Status", 
                    ["open", "confirmed", "resolved", "rejected"], 
                    index=["open", "confirmed", "resolved", "rejected"].index(f.get("review_status", "open")) if f.get("review_status") in ["open", "confirmed", "resolved", "rejected"] else 0,
                    key=f"status_sel_{f['id']}"
                )
            with rc2:
                comment = st.text_input("Reviewer Notes", value=f.get("reviewer_comments") or "", key=f"notes_{f['id']}")
                
            if st.button("💾 Save Review Decision", key=f"save_btn_{f['id']}"):
                try:
                    patch_payload = {"review_status": new_status, "reviewer_comments": comment}
                    patch_res = requests.patch(f"{api_base}/findings/{f['id']}", json=patch_payload)
                    if patch_res.status_code == 200:
                        st.success("Review updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update: {patch_res.text}")
                except Exception as e:
                    st.error(str(e))
else:
    st.info("No architectural findings found matching the criteria. Upload specifications to trigger enterprise rule validation.")

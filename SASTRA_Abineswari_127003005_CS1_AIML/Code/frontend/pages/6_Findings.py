import streamlit as st
import os
import sys
import pandas as pd
import requests
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header, render_empty_state

st.set_page_config(page_title="Findings & Reviews — AUTOSAR AI", page_icon="⚠️", layout="wide")
inject_custom_css()

render_header(
    title="Findings & Verification Reviews",
    subtitle="Automated safety rule validation, architectural compliance & human-in-the-loop review audit trail",
    badge_text="Governance & Audit",
    badge_type="badge-navy"
)

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

tab_findings, tab_audit = st.tabs(["⚠️ Architectural Rule Findings", "📜 Review Audit History"])

# ==============================================================================
# TAB 1: Architectural Rule Findings
# ==============================================================================
with tab_findings:
    with st.container(border=True):
        f1, f2, f3 = st.columns([1, 1.2, 2])
        with f1:
            severity_filter = st.selectbox("Severity Classification", ["All", "High", "Medium", "Low"])
        with f2:
            status_filter = st.selectbox("Review Status", ["All", "open", "confirmed", "resolved", "rejected"])
        with f3:
            search_q = st.text_input("Search Rule Findings", placeholder="Search finding descriptions...")

    findings = []
    try:
        res = requests.get(f"{api_base}/projects/{project_id}/findings", timeout=5)
        if res.status_code == 200:
            findings = res.json()
    except requests.exceptions.ConnectionError:
        st.warning("Backend API server is currently unavailable. Ensure backend is active on http://127.0.0.1:8000.")
    except Exception as e:
        st.error(f"Failed to fetch findings: {str(e)}")

    if severity_filter != "All":
        findings = [f for f in findings if (f.get("severity") or "").lower() == severity_filter.lower()]
    if status_filter != "All":
        findings = [f for f in findings if (f.get("review_status") or "").lower() == status_filter.lower()]
    if search_q.strip():
        findings = [f for f in findings if search_q.strip().lower() in (f.get("description") or "").lower()]

    if findings:
        st.caption(f"Showing {len(findings)} architectural finding(s):")
        for f in findings:
            sev = f.get("severity", "Low")
            sev_class = "badge-error" if sev == "High" else ("badge-pending" if sev == "Medium" else "badge-info")
            r_stat = f.get("review_status", "open")
            status_class = "badge-success" if r_stat == "confirmed" else ("badge-processing" if r_stat == "resolved" else ("badge-error" if r_stat == "rejected" else "badge-pending"))
            
            with st.expander(f"⚠️ [{sev}] {f.get('finding_type', 'Rule Violation')} — {f.get('description', '')[:70]}...", expanded=False):
                fc1, fc2 = st.columns(2)
                with fc1:
                    st.markdown(f"**Finding ID:** `{f['id']}`")
                    st.markdown(f"**Severity:** <span class='badge {sev_class}'>{sev}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Rule Classification:** `{f.get('finding_type')}`")
                with fc2:
                    st.markdown(f"**Review Status:** <span class='badge {status_class}'>{r_stat}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Specification Document ID:** `{f.get('document_id') or 'N/A'}`")
                    
                st.markdown(f"**Description:** {f.get('description')}")
                
                if f.get("evidence_json"):
                    st.markdown("**Evidence / Trace Context:**")
                    st.code(f["evidence_json"], language="json")
                    
                st.markdown("---")
                st.caption("Update Finding Status & Engineer Comments:")
                rc1, rc2 = st.columns([1, 2])
                with rc1:
                    new_status = st.selectbox(
                        "Review Decision", 
                        ["open", "confirmed", "resolved", "rejected"], 
                        index=["open", "confirmed", "resolved", "rejected"].index(r_stat) if r_stat in ["open", "confirmed", "resolved", "rejected"] else 0,
                        key=f"status_sel_{f['id']}"
                    )
                with rc2:
                    comment = st.text_input("Reviewer Notes", value=f.get("reviewer_comments") or "", key=f"notes_{f['id']}")
                    
                if st.button("💾 Save Finding Review", key=f"save_btn_{f['id']}"):
                    try:
                        patch_payload = {"review_status": new_status, "reviewer_comments": comment}
                        patch_res = requests.patch(f"{api_base}/findings/{f['id']}", json=patch_payload)
                        if patch_res.status_code == 200:
                            st.success("Finding review updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to update: {patch_res.text}")
                    except Exception as e:
                        st.error(str(e))
    else:
        render_empty_state(
            icon="✅",
            title="No Findings Match Filter",
            description="No architectural rule violations match the selected criteria. Upload specifications to trigger automated rule evaluation.",
            action_label="Upload Specification",
            page_target="pages/2_Documents.py"
        )

# ==============================================================================
# TAB 2: Review Audit History
# ==============================================================================
with tab_audit:
    with st.container(border=True):
        st.subheader("Query Review Audit History")
        st.caption("Immutable log of engineer sign-offs, decisions, feedback, and architecture corrections:")

        reviews = []
        try:
            r_res = requests.get(f"{api_base}/projects/{project_id}/reviews", timeout=5)
            if r_res.status_code == 200:
                reviews = r_res.json()
        except requests.exceptions.ConnectionError:
            st.warning("Backend API server is currently unavailable.")
        except Exception as e:
            st.error(f"Failed to load reviews: {str(e)}")

        # Summary KPIs
        tot_rev = len(reviews)
        accepted_cnt = sum(1 for r in reviews if r.get("decision") == "Accepted")
        rejected_cnt = sum(1 for r in reviews if r.get("decision") == "Rejected")
        mod_cnt = sum(1 for r in reviews if r.get("decision") == "Needs Modification")

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Reviews", tot_rev)
        k2.metric("Accepted", accepted_cnt)
        k3.metric("Rejected", rejected_cnt)
        k4.metric("Needs Modification", mod_cnt)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # Filters
        af1, af2, af3 = st.columns(3)
        dec_filter = af1.selectbox("Filter Decision", ["All", "Accepted", "Rejected", "Needs Modification"])
        rev_filter = af2.text_input("Filter by Reviewer ID", placeholder="e.g. ENG-01")
        search_rev = af3.text_input("Search Query or Feedback", placeholder="Search text...")

        filtered_rev = reviews
        if dec_filter != "All":
            filtered_rev = [r for r in filtered_rev if r.get("decision") == dec_filter]
        if rev_filter.strip():
            filtered_rev = [r for r in filtered_rev if rev_filter.strip().lower() in (r.get("reviewer_id") or "").lower()]
        if search_rev.strip():
            kw = search_rev.strip().lower()
            filtered_rev = [r for r in filtered_rev if kw in (r.get("question") or "").lower() or kw in (r.get("feedback") or "").lower()]

        if filtered_rev:
            for r in filtered_rev:
                dec = r.get("decision", "Unknown")
                dec_class = "badge-success" if dec == "Accepted" else ("badge-error" if dec == "Rejected" else "badge-pending")
                with st.expander(f"📋 Record #{r['id']} — {dec.upper()} by {r.get('reviewer_id')} ({r.get('reviewed_at', '')[:19]})", expanded=False):
                    rc_col1, rc_col2 = st.columns(2)
                    with rc_col1:
                        st.markdown(f"**Review Record ID:** `{r['id']}`")
                        st.markdown(f"**Sign-Off Decision:** <span class='badge {dec_class}'>{dec}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Reviewer ID:** `{r.get('reviewer_id')}`")
                        st.markdown(f"**Timestamp:** `{r.get('reviewed_at')}`")
                    with rc_col2:
                        st.markdown(f"**Session ID:** `{r.get('session_id')}`")
                        st.markdown(f"**Grounding Score:** `{r.get('grounding_score') or 'N/A'}%`")
                        st.markdown(f"**Confidence Rating:** `{r.get('confidence_level') or 'N/A'}`")

                    st.markdown(f"**Technical Query:**\n> {r.get('question')}")
                    st.markdown(f"**Original Answer Summary:**\n{r.get('answer_summary')}")
                    
                    if r.get("feedback"):
                        st.info(f"**Engineer Feedback:** {r['feedback']}")
                    if r.get("corrections"):
                        st.warning(f"**Corrected Architecture Facts:** {r['corrections']}")
        else:
            render_empty_state(
                icon="📜",
                title="No Review Records Found",
                description="Sign off on AI Assistant responses in the AI Assistant view to populate this audit trail.",
                action_label="Open AI Assistant",
                page_target="pages/4_AI_Assistant.py"
            )

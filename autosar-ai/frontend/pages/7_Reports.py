import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="Reports & Exports", page_icon="📥", layout="wide")
inject_custom_css()

render_header("Reports & Exports", "Generate and download extraction reports")

import requests
import os

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

c1, c2 = st.columns([1, 2])

with c1:
    with st.container(border=True):
        st.subheader("Generate New Report")
        report_type = st.selectbox("Report Type", ["Architecture Summary", "Findings Report", "Dependency Matrix"])
        report_format = st.selectbox("Format", ["CSV", "JSON", "PDF"])
        
        if st.button("Generate Report", use_container_width=True):
            with st.spinner("Compiling project data..."):
                try:
                    payload = {"report_type": report_type, "format": report_format}
                    res = requests.post(f"{api_base}/projects/{project_id}/reports", json=payload)
                    if res.status_code == 200:
                        st.success("Report generated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Generation failed: {res.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with c2:
    with st.container(border=True):
        st.subheader("Generated Reports Repository")
    
    reports = []
    try:
        r_res = requests.get(f"{api_base}/projects/{project_id}/reports")
        if r_res.status_code == 200:
            reports = r_res.json()
    except Exception as e:
        st.error(f"Failed to fetch reports: {str(e)}")

    if reports:
        for r in reports:
            created_str = str(r.get('created_at', ''))[:19]
            fname = os.path.basename(r.get('storage_path', f"report_{r['id']}"))
            with st.expander(f"📊 {r['report_type']} ({r['format']}) — {created_str}", expanded=False):
                st.write(f"**Report ID:** {r['id']}")
                st.write(f"**Format:** `{r['format']}`")
                st.write(f"**File:** `{fname}`")
                
                # Fetch bytes for download
                try:
                    file_res = requests.get(f"{api_base}/reports/{r['id']}/download")
                    if file_res.status_code == 200:
                        mime_type = "text/csv" if r['format'].lower() == "csv" else ("application/json" if r['format'].lower() == "json" else "text/plain")
                        st.download_button(
                            label=f"⬇️ Download {fname}",
                            data=file_res.content,
                            file_name=fname,
                            mime=mime_type,
                            key=f"dl_btn_{r['id']}",
                            use_container_width=True
                        )
                    else:
                        st.warning("Report file is pending or unavailable on disk.")
                except Exception as e:
                    st.error(f"Could not prepare download: {str(e)}")
    else:
        st.info("No reports generated yet. Use the panel on the left to generate one.")

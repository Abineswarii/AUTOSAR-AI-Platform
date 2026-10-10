import streamlit as st

st.set_page_config(page_title="Dashboard - AUTOSAR AI", page_icon="📊", layout="wide")
st.title("Dashboard")

st.markdown("Overview of the active project and system metrics.")

# Placeholder for dashboard metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Uploaded Documents", "0")
col2.metric("Extracted Entities", "0")
col3.metric("Open Findings", "0")
col4.metric("Active Sessions", "0")

st.info("Select a project from the sidebar to view its specific dashboard.")

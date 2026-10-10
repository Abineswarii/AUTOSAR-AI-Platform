import streamlit as st

st.set_page_config(
    page_title="AUTOSAR AI Dashboard",
    page_icon="🚗",
    layout="wide",
)

st.title("AUTOSAR AI — High-Level Design Document Intelligence Platform")
st.markdown("""
Welcome to the AUTOSAR AI platform. This application helps you analyze High-Level Design (HLD) documents.
Please select a page from the sidebar to continue.
""")

st.info("System is starting up or no project is currently selected.")

# We will fetch dashboard metrics from the backend here in subsequent phases.

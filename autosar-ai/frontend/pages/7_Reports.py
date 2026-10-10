import streamlit as st

st.set_page_config(page_title="Reports - AUTOSAR AI", page_icon="📑", layout="wide")
st.title("Reports and Exports")

st.markdown("Generate and download reports for extracted architectures and findings.")

st.selectbox("Select Report Type", ["Document Summary", "Architecture Inventory", "Findings Report"])
st.button("Generate Report")

import streamlit as st

st.set_page_config(page_title="Document Comparison - AUTOSAR AI", page_icon="⚖️", layout="wide")
st.title("Document Comparison")

st.markdown("Compare two versions of an HLD document or two different documents to identify changes.")

col1, col2 = st.columns(2)
with col1:
    st.selectbox("Baseline Document", ["None"])
with col2:
    st.selectbox("Comparison Document", ["None"])

st.button("Compare Documents")

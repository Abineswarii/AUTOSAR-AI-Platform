import streamlit as st

st.set_page_config(page_title="Documents - AUTOSAR AI", page_icon="📄", layout="wide")
st.title("Documents Management")

st.markdown("Upload, view, and process High-Level Design (HLD) documents.")

with st.expander("Upload New Document", expanded=True):
    st.file_uploader("Upload a PDF document", type=["pdf"])
    st.button("Upload and Process")

st.subheader("Document List")
st.info("No documents found in the current project.")

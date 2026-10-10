import streamlit as st

st.set_page_config(page_title="AI Assistant - AUTOSAR AI", page_icon="🤖", layout="wide")
st.title("AI Assistant")

st.markdown("Ask natural-language questions about the uploaded HLD documents.")

query = st.chat_input("Ask a question about the architecture...")
if query:
    st.chat_message("user").write(query)
    st.chat_message("assistant").write("I'm sorry, the AI service is not yet connected.")

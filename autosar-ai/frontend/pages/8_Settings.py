import streamlit as st

st.set_page_config(page_title="Settings - AUTOSAR AI", page_icon="⚙️", layout="wide")
st.title("Settings")

st.markdown("Manage application configuration and project settings.")

st.subheader("Project Settings")
st.text_input("Project Name", "Default Project")
st.button("Save Settings")

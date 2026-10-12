import streamlit as st
import os
import sys
import time
import requests

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header

st.set_page_config(page_title="AI Assistant - AUTOSAR AI", page_icon="🤖", layout="wide")
inject_custom_css()

render_header("AI Assistant", "Grounded automotive engineering document intelligence")

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

# Fetch project documents for scoping
docs = []
try:
    d_res = requests.get(f"{api_base}/projects/{project_id}/documents")
    if d_res.status_code == 200:
        docs = d_res.json()
except Exception:
    pass

doc_options = {d["original_filename"]: d["id"] for d in docs if d["status"] == "READY"}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Top Banner showing active local model
col_banner1, col_banner2 = st.columns([2, 1])
with col_banner1:
    st.markdown("""
    <div style='background-color: #EFF6FF; border: 1px solid #DBEAFE; border-radius: 8px; padding: 10px 14px; margin-bottom: 16px;'>
        <span style='color: #1D4ED8; font-weight: 600; font-size: 0.9rem;'>🤖 Local Engine: Ollama llama3.2:3b</span>
        <span style='color: #6B7280; font-size: 0.85rem; margin-left: 12px;'>• Local Offline Inference • Privacy Preserving</span>
    </div>
    """, unsafe_allow_html=True)
with col_banner2:
    selected_doc_name = st.selectbox(
        "Scope Analysis", 
        ["All Project Documents"] + list(doc_options.keys()),
        label_visibility="collapsed"
    )

selected_doc_ids = []
if selected_doc_name != "All Project Documents" and selected_doc_name in doc_options:
    selected_doc_ids = [doc_options[selected_doc_name]]

col_chat, col_sidebar = st.columns([3, 1])

with col_chat:
    # Render message history
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align: center; padding: 40px 20px; color: #6B7280;'>
            <div style='font-size: 2.5rem; margin-bottom: 10px;'>💬</div>
            <h4 style='color: #111827; margin-bottom: 6px;'>Engineering Assistant Ready</h4>
            <p style='font-size: 0.95rem;'>Ask about software components, runnables, interfaces, or architectural compliance constraints.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("citations"):
                    with st.expander(f"📚 Source Citations ({len(message['citations'])})", expanded=False):
                        for c in message["citations"]:
                            doc_title = c.get('document_name') or f"Doc #{c.get('document_id')}"
                            p_start = c.get('page_start', 1)
                            p_end = c.get('page_end', 1)
                            st.markdown(f"**{doc_title}** — *Page {p_start} to {p_end}*")
                            if c.get("content"):
                                st.caption(f"> \"{c['content'][:250]}...\"")

    def handle_query(query_text: str):
        st.chat_message("user").markdown(query_text)
        st.session_state.messages.append({"role": "user", "content": query_text})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing document evidence via Ollama (llama3.2:3b)..."):
                try:
                    payload = {"query": query_text, "document_ids": selected_doc_ids}
                    res = requests.post(f"{api_base}/projects/{project_id}/ask", json=payload, timeout=125)
                    if res.status_code == 200:
                        data = res.json()
                        answer = data.get("answer", "No answer returned.")
                        citations = data.get("citations", [])
                    else:
                        answer = f"Ollama / API Error ({res.status_code}): {res.text}"
                        citations = []
                except requests.exceptions.Timeout:
                    answer = "Ollama model generation timed out. The local model is busy or processing large contexts."
                    citations = []
                except Exception as e:
                    answer = f"Failed to communicate with backend: {str(e)}"
                    citations = []
                
                st.markdown(answer)
                if citations:
                    with st.expander(f"📚 Source Citations ({len(citations)})", expanded=False):
                        for c in citations:
                            doc_title = c.get('document_name') or f"Doc #{c.get('document_id')}"
                            p_start = c.get('page_start', 1)
                            p_end = c.get('page_end', 1)
                            st.markdown(f"**{doc_title}** — *Page {p_start} to {p_end}*")
                            if c.get("content"):
                                st.caption(f"> \"{c['content'][:250]}...\"")
                                
        st.session_state.messages.append({"role": "assistant", "content": answer, "citations": citations})
        st.rerun()

    # Chat prompt input
    if prompt := st.chat_input("Ask about software components, interfaces, or design decisions..."):
        handle_query(prompt)

with col_sidebar:
    with st.container(border=True):
        st.subheader("Suggested Questions")
        st.caption("Click any prompt below to query your uploaded specifications:")
        
        suggested = [
            "Summarize the AUTOSAR architecture.",
            "List all extracted Software Components.",
            "Which interfaces and runnables are defined?",
            "Are there any circular dependencies detected?",
            "Explain any insecure IPC communication patterns."
        ]
        for idx, sq in enumerate(suggested):
            if st.button(sq, key=f"sq_{idx}", use_container_width=True):
                handle_query(sq)
                
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

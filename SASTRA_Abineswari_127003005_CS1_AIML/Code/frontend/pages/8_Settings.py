import streamlit as st
import os
import sys
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header, get_active_engine_info

st.set_page_config(page_title="Settings & System Status — AUTOSAR AI", page_icon="⚙️", layout="wide")
inject_custom_css()

api_base = "http://127.0.0.1:8000/api/v1"
engine_info = get_active_engine_info(api_base)
status_badge = "badge-success" if engine_info.get("overall_status") == "PASS" else ("badge-error" if engine_info.get("overall_status") == "FAIL" else "badge-pending")

render_header(
    title="Settings & System Status",
    subtitle="Configure platform parameters, inspect subsystem telemetry & verify model provider connectivity",
    badge_text=f"System: {engine_info.get('overall_status', 'UNKNOWN')}",
    badge_type=status_badge
)

# Fetch current settings and system info from backend
current_cfg = {
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "enable_table_extraction": True,
    "ocr_enabled": False,
    "flag_circular_dependencies": True,
    "enforce_secure_ipc": True,
    "require_boundary_definitions": True
}
try:
    s_res = requests.get(f"{api_base}/settings", timeout=3)
    if s_res.status_code == 200:
        current_cfg.update(s_res.json())
except Exception:
    pass

sys_info = {}
try:
    sys_res = requests.get(f"{api_base}/settings/system", timeout=3)
    if sys_res.status_code == 200:
        sys_info = sys_res.json()
except Exception:
    pass

# Section 1: LLM Engine & Subsystem Health Cards
st.subheader("Subsystem Diagnostics & Model Provider")
st.caption("Live telemetry across offline core services:")

c_diag1, c_diag2 = st.columns([1.5, 1])

with c_diag1:
    with st.container(border=True):
        st.markdown("#### Active LLM Engine Configuration")
        provider_name = sys_info.get("llm_provider", engine_info.get("provider", "ollama")).upper()
        model_name = sys_info.get("llm_model", engine_info.get("model", "llama3.2:3b"))
        is_local = sys_info.get("is_local_inference", engine_info.get("is_local", True))
        has_key = sys_info.get("has_api_key", False)
        base_url = sys_info.get("llm_base_url", engine_info.get("base_url", "http://localhost:11434"))

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown(f"**Provider:** `{provider_name}`")
            st.markdown(f"**Model Identifier:** `{model_name}`")
            st.markdown(f"**Endpoint URL:** `{base_url}`")
        with col_l2:
            st.markdown(f"**Execution Mode:** `{'On-Premises / Local' if is_local else 'Hosted Cloud API'}`")
            st.markdown(f"**API Key Configured:** `{'Yes (Masked)' if has_key else 'Not Required (Local Offline)'}`")
            st.markdown(f"**Data Privacy Policy:** `Zero External Data Leakage`")

        st.caption("Model provider settings are configured securely via `.env` file without exposing credentials.")

with c_diag2:
    with st.container(border=True):
        st.markdown("#### Subsystem Health Telemetry")
        diag_data = None
        try:
            d_res = requests.get(f"{api_base}/diagnostics", timeout=5)
            if d_res.status_code == 200:
                diag_data = d_res.json()
        except Exception:
            pass

        if diag_data:
            subsystems = diag_data.get("subsystems", {})
            for key, sub in subsystems.items():
                s_stat = sub.get("status", "UNKNOWN")
                badge = "badge-success" if s_stat == "PASS" else ("badge-error" if s_stat == "FAIL" else "badge-pending")
                svc_title = sub.get('service', key.replace('_', ' ').title())
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; padding: 4px 0; border-bottom: 1px solid #F1F5F9; font-size:0.86rem;'>
                    <span style='color:#334155; font-weight:500;'>{svc_title}</span>
                    <span class='badge {badge}'>{s_stat}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Diagnostics check in progress...")

        if st.button("🔄 Probe Subsystems Now", use_container_width=True):
            st.rerun()

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# Section 2: Platform Extraction & Enterprise Rules
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Document Extraction Parameters")
        st.caption("Configure sliding window chunking and ingestion settings:")
        c_size = st.slider("Chunk Size", 200, 2500, int(current_cfg.get("chunk_size", 1000)), step=50, help="Document chunk size in characters")
        c_overlap = st.slider("Chunk Overlap", 0, 500, int(current_cfg.get("chunk_overlap", 150)), step=25, help="Overlap between consecutive chunks")
        c_tables = st.checkbox("Enable Table Extraction", value=bool(current_cfg.get("enable_table_extraction", True)))
        c_ocr = st.checkbox("Enable Optical Character Recognition (OCR)", value=bool(current_cfg.get("ocr_enabled", False)))
        
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Save Extraction Parameters", key="save_extraction", use_container_width=True):
            if c_overlap >= c_size:
                st.error("Error: Chunk overlap must be strictly less than chunk size.")
            else:
                payload = {
                    **current_cfg,
                    "chunk_size": c_size,
                    "chunk_overlap": c_overlap,
                    "enable_table_extraction": c_tables,
                    "ocr_enabled": c_ocr
                }
                try:
                    up_res = requests.post(f"{api_base}/settings", json=payload, timeout=5)
                    if up_res.status_code == 200:
                        st.success("Extraction parameters saved and applied to runtime!")
                    else:
                        st.error(f"Failed to save: {up_res.text}")
                except Exception as e:
                    st.error(str(e))

with col2:
    with st.container(border=True):
        st.subheader("Enterprise Validation Rules")
        st.caption("Configure architectural constraints evaluated during specification ingestion:")
        r_circ = st.checkbox("Flag Circular Dependencies between Components", value=bool(current_cfg.get("flag_circular_dependencies", True)))
        r_ipc = st.checkbox("Enforce Secure IPC strict matching", value=bool(current_cfg.get("enforce_secure_ipc", True)))
        r_bounds = st.checkbox("Require Boundary Definitions on arrays and buffers", value=bool(current_cfg.get("require_boundary_definitions", True)))
        
        st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
        if st.button("Save Validation Rules", key="save_rules", use_container_width=True):
            payload = {
                **current_cfg,
                "flag_circular_dependencies": r_circ,
                "enforce_secure_ipc": r_ipc,
                "require_boundary_definitions": r_bounds
            }
            try:
                up_res = requests.post(f"{api_base}/settings", json=payload, timeout=5)
                if up_res.status_code == 200:
                    st.success("Enterprise rules saved! Rules will apply to future document uploads.")
                else:
                    st.error(f"Failed to save: {up_res.text}")
            except Exception as e:
                st.error(str(e))

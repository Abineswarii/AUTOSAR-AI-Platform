import streamlit as st
import requests
from typing import Optional, Dict, Any

def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Enterprise Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* Global Typography & Base Colors */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #0F172A;
            -webkit-font-smoothing: antialiased;
        }

        code, pre, .stCodeBlock {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Top Bar / Main App Background */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1E293B !important;
        }

        [data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }

        /* Sidebar Navigation Hover & Active States */
        [data-testid="stSidebarNav"] a {
            padding: 8px 14px !important;
            margin-bottom: 3px !important;
            border-radius: 6px !important;
            color: #94A3B8 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease-in-out !important;
        }

        [data-testid="stSidebarNav"] a:hover {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #1E3A8A !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
        }

        /* Buttons (Primary - Cobalt Blue) */
        .stButton>button {
            background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            border: 1px solid #1D4ED8 !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 1.15rem !important;
            transition: all 0.18s ease-in-out !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08) !important;
        }
        .stButton>button:hover {
            background: linear-gradient(180deg, #1D4ED8 0%, #1E40AF 100%) !important;
            border-color: #1E40AF !important;
            box-shadow: 0 3px 6px -1px rgba(37, 99, 235, 0.25) !important;
            transform: translateY(-0.5px);
        }
        .stButton>button:active {
            transform: translateY(0.5px);
        }

        /* Download Buttons */
        .stDownloadButton>button {
            background-color: #FFFFFF !important;
            color: #1E3A8A !important;
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
            padding: 0.45rem 1.1rem !important;
            transition: all 0.18s ease-in-out !important;
        }
        .stDownloadButton>button:hover {
            background-color: #EFF6FF !important;
            border-color: #93C5FD !important;
            color: #1D4ED8 !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            position: relative;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.85rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            letter-spacing: -0.02em !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.82rem !important;
            color: #64748B !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
        }

        /* Headings */
        h1 {
            color: #0F172A !important;
            font-weight: 700 !important;
            font-size: 1.85rem !important;
            letter-spacing: -0.025em !important;
        }
        h2 {
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 1.35rem !important;
            letter-spacing: -0.02em !important;
        }
        h3 {
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 1.12rem !important;
            letter-spacing: -0.015em !important;
        }
        h4, h5, h6 {
            color: #334155 !important;
            font-weight: 600 !important;
        }

        /* Streamlit Container Cards */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
            padding: 0.25rem !important;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #F8FAFC !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            color: #1E293B !important;
            border: 1px solid #E2E8F0 !important;
        }
        .streamlit-expanderHeader:hover {
            background-color: #F1F5F9 !important;
            color: #0F172A !important;
        }

        /* Form Controls */
        .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            font-size: 0.9rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
        }

        /* DataFrames */
        [data-testid="stDataFrame"] {
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
            background-color: #FFFFFF !important;
        }

        /* Chat Messages */
        [data-testid="stChatMessage"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            padding: 1.1rem !important;
            margin-bottom: 0.85rem !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            padding: 0 16px;
            border-radius: 6px 6px 0 0;
            font-weight: 500;
            font-size: 0.92rem;
            color: #64748B;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #1E3A8A !important;
            font-weight: 600 !important;
            border-bottom: 2px solid #2563EB !important;
        }

        /* Enterprise Badges & Pills */
        .badge {
            display: inline-block;
            padding: 2px 9px;
            border-radius: 9999px;
            font-size: 0.76rem;
            font-weight: 600;
            line-height: 1.4;
            letter-spacing: 0.02em;
        }
        .badge-success { background-color: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }
        .badge-processing { background-color: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }
        .badge-pending { background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
        .badge-error { background-color: #FEE2E2; color: #B91C1C; border: 1px solid #FECACA; }
        .badge-info { background-color: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
        .badge-neutral { background-color: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }
        .badge-navy { background-color: #EFF6FF; color: #1E3A8A; border: 1px solid #DBEAFE; }

        /* Tables inside custom HTML */
        .sa-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }
        .sa-table th {
            padding: 10px 12px;
            background-color: #F8FAFC;
            color: #475569;
            font-weight: 600;
            border-bottom: 1px solid #E2E8F0;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .sa-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #F1F5F9;
            color: #1E293B;
        }
        .sa-table tr:hover td {
            background-color: #F8FAFC;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: Optional[str] = None, badge_text: Optional[str] = None, badge_type: str = "badge-navy"):
    """
    Renders an enterprise page header with clean typography, subtitle, and optional status badge.
    """
    badge_html = f"<span class='badge {badge_type}' style='vertical-align:middle; margin-left:12px;'>{badge_text}</span>" if badge_text else ""
    sub_html = f"<p style='color:#64748B; font-size:0.96rem; margin-top:-4px; margin-bottom:0;'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
        <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:18px 24px; margin-bottom:1.5rem; box-shadow:0 1px 2px rgba(15,23,42,0.03);'>
            <div style='display:flex; align-items:center;'>
                <h1 style='color:#0F172A; font-weight:700; font-size:1.75rem; margin:0; line-height:1.2;'>{title}</h1>
                {badge_html}
            </div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60, show_spinner=False)
def get_active_engine_info(api_base: str = "http://127.0.0.1:8000/api/v1") -> Dict[str, Any]:
    """
    Fetches real active LLM and platform configuration from backend without blocking UI navigation.
    Caches for 60 seconds with show_spinner=False to keep page navigation instantaneous and silent,
    completely eliminating technical 'Running get_active_engine_info(...)' loading displays.
    """
    try:
        s_res = requests.get(f"{api_base}/settings/system", timeout=1.5)
        if s_res.status_code == 200:
            s_data = s_res.json()
            provider = s_data.get("llm_provider", "ollama")
            model = s_data.get("llm_model", "llama3.2:3b")
            base_url = s_data.get("llm_base_url", "http://localhost:11434")
            is_local = s_data.get("is_local_inference", True)
            has_key = s_data.get("has_api_key", False)

            reachable = True
            if provider == "gemini" and not has_key:
                reachable = False

            return {
                "provider": provider,
                "model": model,
                "base_url": base_url,
                "is_local": is_local,
                "status": "PASS" if reachable else "BLOCKED",
                "reachable": reachable,
                "overall_status": "PASS",
                "subsystems": {}
            }
    except Exception:
        pass

    return {
        "provider": "ollama",
        "model": "llama3.2:3b",
        "base_url": "http://localhost:11434",
        "is_local": True,
        "status": "OFFLINE",
        "reachable": False,
        "overall_status": "OFFLINE",
        "subsystems": {}
    }

def render_engine_banner(engine_info: Dict[str, Any]):
    """
    Displays a standardized, dynamic engine status banner without hardcoded strings.
    """
    provider = engine_info.get("provider", "ollama").upper()
    model = engine_info.get("model", "llama3.2:3b")
    is_local = engine_info.get("is_local", True)
    mode_text = "Local On-Premises • Zero External Data Leakage" if is_local else "Secure Hosted API • Read-Only Analysis"
    badge_class = "badge-success" if engine_info.get("reachable") else "badge-error"
    badge_label = "ONLINE" if engine_info.get("reachable") else "DISCONNECTED"

    st.markdown(f"""
    <div style='background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px; padding:10px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <span style='color:#1E3A8A; font-weight:700; font-size:0.92rem;'>Engine: {provider} ({model})</span>
            <span style='color:#475569; font-size:0.83rem; margin-left:12px;'>• {mode_text}</span>
        </div>
        <span class='badge {badge_class}'>{badge_label}</span>
    </div>
    """, unsafe_allow_html=True)

def render_empty_state(icon: str, title: str, description: str, action_label: Optional[str] = None, page_target: Optional[str] = None):
    """
    Renders a clean, friendly empty state card with guidance on how to populate data.
    """
    st.markdown(f"""
    <div style='background:#FFFFFF; border:1px dashed #CBD5E1; border-radius:8px; padding:36px 20px; text-align:center;'>
        <div style='font-size:2rem; margin-bottom:10px;'>{icon}</div>
        <h4 style='color:#1E293B; margin-bottom:6px; font-weight:600;'>{title}</h4>
        <p style='color:#64748B; font-size:0.9rem; max-width:480px; margin:0 auto 16px auto;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)
    if action_label and page_target:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(action_label, use_container_width=True):
                st.switch_page(page_target)

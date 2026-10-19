import streamlit as st
import os
import sys
import pandas as pd
import requests

# Ensure backend imports can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from frontend.utils.ui import inject_custom_css, render_header, render_empty_state

st.set_page_config(page_title="Architecture Explorer — AUTOSAR AI", page_icon="🧩", layout="wide")
inject_custom_css()

render_header(
    title="Architecture Explorer",
    subtitle="Software Component Inventory, Ports/Signals, Dependency Topology & Downstream Change Impact",
    badge_text="Traceability Engine",
    badge_type="badge-navy"
)

project_id = 1
api_base = "http://127.0.0.1:8000/api/v1"

tab_swc, tab_ports, tab_graph = st.tabs([
    "🧩 SWCs & Interfaces", 
    "🚪 Ports & Signals", 
    "🗺️ Topology Graph & Change Impact"
])

# ==============================================================================
# TAB 1: SWCs & Interfaces
# ==============================================================================
with tab_swc:
    with st.container(border=True):
        col_f1, col_f2 = st.columns([1, 2.5])
        with col_f1:
            type_filter = st.selectbox("Entity Classification", ["All", "Software Component", "Runnable", "Interface"])
        with col_f2:
            search_q = st.text_input("Search Components / Interfaces", placeholder="e.g. PowertrainManager_SWC")

    entities = []
    try:
        res = requests.get(f"{api_base}/projects/{project_id}/entities", timeout=5)
        if res.status_code == 200:
            entities = res.json()
    except Exception as e:
        st.error(f"Error fetching architectural entities: {str(e)}")

    # Filter out Ports & Signals from SWC tab (they have their own dedicated tab)
    swc_entities = [e for e in entities if e.get("entity_type") in ["Software Component", "Runnable", "Interface"]]

    if type_filter != "All":
        swc_entities = [e for e in swc_entities if e.get("entity_type") == type_filter]
    if search_q.strip():
        swc_entities = [e for e in swc_entities if search_q.strip().lower() in e.get("name", "").lower()]

    if swc_entities:
        st.caption(f"Showing {len(swc_entities)} software architectural entities:")
        for e in swc_entities:
            etype = e.get("entity_type", "Component")
            r_status = e.get("review_status", "pending")
            status_badge = "badge-success" if r_status == 'confirmed' else ("badge-error" if r_status == 'rejected' else "badge-pending")
            with st.expander(f"🧩 [{etype}] {e.get('name', 'Unknown')}  —  {r_status.upper()}", expanded=False):
                info_c1, info_c2 = st.columns(2)
                with info_c1:
                    st.markdown(f"**Entity Classification:** `{etype}`")
                    st.markdown(f"**Identifier Name:** `{e.get('name')}`")
                    conf_pct = round((e.get('confidence') or 0.9) * 100)
                    st.markdown(f"**Extraction Confidence:** `{conf_pct}%`")
                    st.markdown(f"**Source Specification Page:** Page {e.get('source_page') or 'N/A'}")
                with info_c2:
                    st.markdown(f"**Review Status:** <span class='badge {status_badge}'>{r_status}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Extraction Provenance:** `{e.get('extraction_method', 'engineering_heuristics')}`")
                    
                if e.get("source_excerpt"):
                    st.markdown("**Source Excerpt:**")
                    st.code(e["source_excerpt"], language="text")
                    
                # Entity Review Actions
                st.markdown("---")
                st.caption("Human-in-the-Loop Review Decision:")
                rev_c1, rev_c2, rev_c3 = st.columns(3)
                with rev_c1:
                    if st.button("✅ Confirm Entity", key=f"conf_{e['id']}", use_container_width=True):
                        requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "confirmed"})
                        st.success("Marked as Confirmed!")
                        st.rerun()
                with rev_c2:
                    if st.button("❌ Reject Entity", key=f"rej_{e['id']}", use_container_width=True):
                        requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "rejected"})
                        st.warning("Marked as Rejected.")
                        st.rerun()
                with rev_c3:
                    if st.button("⏳ Reset Pending", key=f"rst_{e['id']}", use_container_width=True):
                        requests.post(f"{api_base}/entities/{e['id']}/review", json={"status": "pending"})
                        st.info("Reset to Pending.")
                        st.rerun()
    else:
        render_empty_state(
            icon="🧩",
            title="No Entities Found",
            description="No architectural entities match your search filter. Ingest an AUTOSAR HLD document to extract components.",
            action_label="Upload Specification",
            page_target="pages/2_Documents.py"
        )

# ==============================================================================
# TAB 2: Ports & Signals
# ==============================================================================
with tab_ports:
    with st.container(border=True):
        st.subheader("Port & Signal Definitions")
        st.caption("Inspect extracted AUTOSAR Ports (PPort/RPort), directions, interfaces, and carried signal data types:")

        # Fetch ports and signals
        ps_data = []
        try:
            ps_res = requests.get(f"{api_base}/projects/{project_id}/ports_and_signals", timeout=5)
            if ps_res.status_code == 200:
                ps_data = ps_res.json()
        except Exception as e:
            st.error(f"Error fetching ports and signals: {str(e)}")

        # Filter controls
        f_p1, f_p2, f_p3 = st.columns(3)
        available_comps = sorted(list({p.get("component") for p in ps_data if p.get("component") and p.get("component") != "Unassigned"}))
        comp_filter = f_p1.selectbox("Filter by Owning SWC", ["All"] + available_comps)
        dir_filter = f_p2.selectbox("Port Direction", ["All", "Input", "Output", "InOut", "N/A"])
        search_ps = f_p3.text_input("Search Port or Signal Identifier", placeholder="e.g. Port_VehicleSpeed")

        filtered_ps = ps_data
        if comp_filter != "All":
            filtered_ps = [p for p in filtered_ps if p.get("component") == comp_filter]
        if dir_filter != "All":
            filtered_ps = [p for p in filtered_ps if p.get("direction") == dir_filter]
        if search_ps.strip():
            kw = search_ps.strip().lower()
            filtered_ps = [p for p in filtered_ps if kw in (p.get("name") or "").lower() or kw in (p.get("carried_signals") or "").lower()]

        if filtered_ps:
            df_ps = pd.DataFrame([{
                "ID": p.get("id"),
                "Type": p.get("type"),
                "Identifier": p.get("name"),
                "Owning SWC": p.get("component"),
                "Direction": p.get("direction"),
                "Interface": p.get("interface"),
                "Carried Signals": p.get("carried_signals"),
                "Data Type": p.get("signal_data_type"),
                "Version": p.get("version"),
                "Page": p.get("source_page"),
                "Review Status": p.get("review_status")
            } for p in filtered_ps])
            st.dataframe(df_ps, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(filtered_ps)} of {len(ps_data)} architectural port and signal records.")
        else:
            render_empty_state(
                icon="🚪",
                title="No Ports or Signals Identified",
                description="Upload an AUTOSAR specification with explicit port declarations (e.g. PPort_*, RPort_*, Signal_*) to populate this table.",
                action_label="Upload Specification",
                page_target="pages/2_Documents.py"
            )

# ==============================================================================
# TAB 3: Topology Graph & Dependency Change Impact
# ==============================================================================
with tab_graph:
    with st.container(border=True):
        st.subheader("Architectural Topology Diagram")
        st.caption("Visual representation of validated component dependencies, interfaces, and port linkages:")

        topo_data = {}
        try:
            topo_res = requests.get(f"{api_base}/projects/{project_id}/topology", timeout=5)
            if topo_res.status_code == 200:
                topo_data = topo_res.json()
        except Exception as e:
            st.error(f"Error loading topology: {str(e)}")

        mermaid_code = topo_data.get("mermaid_code", "graph TD\n    empty[\"No architectural entities available\"]")

        # Proper Mermaid Block in Streamlit Markdown
        st.markdown(f"""```mermaid
{mermaid_code}
```""")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col_edges, col_impact = st.columns([1, 1])

    with col_edges:
        with st.container(border=True):
            st.subheader("Directed Relationship Edges")
            st.caption("Extracted architectural linkages stored in SQLite:")
            edges = topo_data.get("edges", [])
            if edges:
                df_edges = pd.DataFrame([{
                    "Source Entity": e.get("source"),
                    "Relationship": e.get("relationship_type"),
                    "Target Entity": e.get("target"),
                    "Source Page": e.get("source_page"),
                    "Status": e.get("review_status")
                } for e in edges])
                st.dataframe(df_edges, use_container_width=True, hide_index=True)
            else:
                st.info("No relationship edges extracted yet.")

    with col_impact:
        with st.container(border=True):
            st.subheader("🔍 Change Impact Traversal (BFS)")
            st.caption("Select a modified component to trace direct and transitive downstream dependents:")
            
            all_swc_names = [e.get("name") for e in entities if e.get("entity_type") == "Software Component"]
            if all_swc_names:
                selected_root = st.selectbox("Modified Root Component", all_swc_names)
                if st.button("Execute Change Impact Traversal", use_container_width=True):
                    try:
                        imp_res = requests.get(f"{api_base}/projects/{project_id}/impact", params={"root_entity_name": selected_root}, timeout=5)
                        if imp_res.status_code == 200:
                            imp = imp_res.json()
                            tot_impacted = imp.get("total_impacted_count", 0)
                            st.markdown(f"**Total Impacted Dependents:** `{tot_impacted}`")
                            
                            if imp.get("direct_dependents"):
                                st.markdown("**Direct Dependents (1-hop):**")
                                for d in imp["direct_dependents"]:
                                    st.markdown(f"- 🔴 `{d}`")
                            else:
                                st.caption("No direct 1-hop dependents.")

                            if imp.get("transitive_dependents"):
                                st.markdown("**Transitive Downstream Dependents (>1 hops):**")
                                for td in imp["transitive_dependents"]:
                                    st.markdown(f"- 🟠 `{td}`")

                            if imp.get("impact_paths"):
                                with st.expander("Dependency Propagation Paths", expanded=True):
                                    for p in imp["impact_paths"]:
                                        st.code(p, language="text")

                            if imp.get("cycle_detected"):
                                st.warning("⚠️ Circular dependency detected during graph traversal. Traversal protected against infinite loop.")
                    except Exception as e:
                        st.error(f"Impact calculation error: {str(e)}")
            else:
                st.info("No software components available for impact analysis.")

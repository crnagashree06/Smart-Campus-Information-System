"""Module 07 — Directory Scanning with Exception Handling"""
import streamlit as st

class MissingFileOrFolderError(Exception):
    pass

def render():
    st.markdown('<span class="section-tag">os · exception handling · user-defined exceptions</span>', unsafe_allow_html=True)
    st.subheader("07 · Directory Scanning with Exception Handling")

    if "m7_tree" not in st.session_state:
        st.session_state.m7_tree = {"folders": [], "files": {}}

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Define Directory Structure**")
        fa, fb = st.columns([4, 1])
        with fa: fname = st.text_input("Folder", placeholder="e.g. Student1", key="m7_folder", label_visibility="collapsed")
        with fb:
            if st.button("+ Folder", key="m7_add_folder"):
                if fname.strip() and fname.strip() not in st.session_state.m7_tree["folders"]:
                    st.session_state.m7_tree["folders"].append(fname.strip())
                    st.session_state.m7_tree["files"][fname.strip()] = []
                    st.rerun()

        if st.session_state.m7_tree["folders"]:
            ca, cb, cc = st.columns([2, 3, 1])
            with ca: parent = st.selectbox("Parent", st.session_state.m7_tree["folders"], key="m7_parent", label_visibility="collapsed")
            with cb: ffile  = st.text_input("File", placeholder="e.g. report.pdf", key="m7_file", label_visibility="collapsed")
            with cc:
                if st.button("+ File", key="m7_add_file"):
                    if ffile.strip():
                        st.session_state.m7_tree["files"].setdefault(parent, []).append(ffile.strip()); st.rerun()

            tree_html = "<div style='font-family:DM Mono,monospace;font-size:0.8rem;line-height:2;background:#fdf6ec;padding:0.8rem;border-radius:10px;border:1px solid #c9a978'>"
            for f in st.session_state.m7_tree["folders"]:
                tree_html += f"<span style='color:#6b3a1f;font-weight:700'>📁 {f}/</span><br>"
                for fi in st.session_state.m7_tree["files"].get(f, []):
                    tree_html += f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#8b6340'>📄 {fi}</span><br>"
                if not st.session_state.m7_tree["files"].get(f):
                    tree_html += "<span style='padding-left:1.2rem;color:#b09070;font-size:0.72rem'>(empty)</span><br>"
            tree_html += "</div>"
            st.markdown(tree_html, unsafe_allow_html=True)
        else:
            st.caption("No structure defined yet.")

        b1, b2 = st.columns(2)
        with b1: run = st.button("▶  Scan", key="m7_run", type="primary")
        with b2:
            if st.button("Clear", key="m7_clear"):
                st.session_state.m7_tree = {"folders": [], "files": {}}; st.rerun()

    with col_out:
        st.markdown("**Result**")
        if run:
            tree = st.session_state.m7_tree
            if not tree["folders"]:
                st.error("No directory structure defined.")
            else:
                empty = [f for f in tree["folders"] if not tree["files"].get(f)]
                folder_rows = ""
                for f in tree["folders"]:
                    files = tree["files"].get(f, [])
                    file_list = " · ".join(files) if files else "(empty)"
                    color = "#c0392b" if not files else "#6b3a1f"
                    folder_rows += f'<div class="result-row"><span class="result-label" style="color:{color}">📁 {f}</span><span class="result-value" style="font-size:0.8rem;color:{color}">{file_list}</span></div>'

                status_html = ""
                if empty:
                    status_html = f'<div class="result-row" style="background:#fce8e8;margin-top:0.6rem"><span class="result-label" style="color:#c0392b">⚠ Error</span><span class="result-value" style="color:#c0392b;font-size:0.82rem">MissingFileOrFolderError: {", ".join(empty)}</span></div>'
                else:
                    status_html = '<div class="result-row" style="background:#3b2007;margin-top:0.6rem"><span class="result-label" style="color:#c9a978">Status</span><span class="result-value" style="color:#a8d8a0">✔ Scan complete — no errors</span></div>'

                st.markdown(f"""
                <div class="output-card">
                  <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#8b6340;margin-bottom:0.8rem">Projects/ directory scan</div>
                  {folder_rows}
                  {status_html}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Build a directory tree and click Scan</span></div>', unsafe_allow_html=True)

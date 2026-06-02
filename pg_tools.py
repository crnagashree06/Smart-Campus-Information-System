"""System Tools — Directory Scanner + File Manager (admin section)"""
import streamlit as st, os

class MissingFileOrFolderError(Exception):
    pass

def tab_directory():
    st.markdown('<span class="section-tag">os · exception handling · user-defined exceptions</span>', unsafe_allow_html=True)
    tree = st.session_state.m7_tree

    col_in, col_out = st.columns(2, gap="large")
    with col_in:
        st.markdown("**Build a Directory Structure**")
        fa, fb = st.columns([4,1])
        with fa: fname = st.text_input("Folder", placeholder="e.g. Student_Projects", key="dt_folder", label_visibility="collapsed")
        with fb:
            if st.button("+ Folder", key="dt_add_folder"):
                if fname.strip() and fname.strip() not in tree["folders"]:
                    tree["folders"].append(fname.strip())
                    tree["files"][fname.strip()] = []
                    st.session_state.m7_tree = tree; st.rerun()

        if tree["folders"]:
            ca, cb, cc = st.columns([2,3,1])
            with ca: parent = st.selectbox("Parent", tree["folders"], key="dt_parent", label_visibility="collapsed")
            with cb: ffile  = st.text_input("File", placeholder="e.g. report.pdf", key="dt_file", label_visibility="collapsed")
            with cc:
                if st.button("+ File", key="dt_add_file"):
                    if ffile.strip():
                        tree["files"].setdefault(parent,[]).append(ffile.strip())
                        st.session_state.m7_tree = tree; st.rerun()

            tree_html = "<div style='font-family:DM Mono,monospace;font-size:0.8rem;line-height:2;background:#fdf6ec;padding:0.8rem;border-radius:10px;border:1px solid #c9a978'>"
            for f in tree["folders"]:
                tree_html += f"<span style='color:#6b3a1f;font-weight:700'>📁 {f}/</span><br>"
                for fi in tree["files"].get(f,[]):
                    tree_html += f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#8b6340'>📄 {fi}</span><br>"
                if not tree["files"].get(f):
                    tree_html += "<span style='padding-left:1.2rem;color:#b09070;font-size:0.72rem'>(empty)</span><br>"
            tree_html += "</div>"
            st.markdown(tree_html, unsafe_allow_html=True)
        else:
            st.caption("No structure defined yet.")

        b1, b2 = st.columns(2)
        with b1: run = st.button("▶  Scan", key="dt_run", type="primary")
        with b2:
            if st.button("Clear", key="dt_clear"):
                st.session_state.m7_tree = {"folders":[],"files":{}}; st.rerun()

    with col_out:
        if run:
            if not tree["folders"]: st.error("No structure defined.")
            else:
                empty = [f for f in tree["folders"] if not tree["files"].get(f)]
                folder_rows = "".join(
                    f'<div class="result-row"><span class="result-label" style="color:{"#c0392b" if f in empty else "#6b3a1f"}">📁 {f}</span>'
                    f'<span class="result-value" style="font-size:0.78rem;color:{"#c0392b" if f in empty else "#3b2007"}">'
                    f'{(" · ".join(tree["files"].get(f,[]))) or "(empty)"}</span></div>'
                    for f in tree["folders"]
                )
                try:
                    if empty: raise MissingFileOrFolderError(f"Empty folder(s): {', '.join(empty)}")
                    status = '<div class="result-row" style="background:#3b2007"><span class="result-label" style="color:#c9a978">Status</span><span class="result-value" style="color:#a8d898">✔ No errors</span></div>'
                except MissingFileOrFolderError as e:
                    status = f'<div class="result-row" style="background:#5a1010"><span class="result-label" style="color:#f0a0a0">⚠ Error</span><span class="result-value" style="color:#ffd0d0;font-size:0.8rem">MissingFileOrFolderError: {e}</span></div>'

                st.markdown(f"""
                <div class="output-card">
                  <div style="font-family:DM Mono,monospace;font-size:0.62rem;text-transform:uppercase;
                              letter-spacing:0.1em;color:#8b6340;margin-bottom:0.8rem">Projects/ scan</div>
                  {folder_rows}{status}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Build a tree and click Scan</span></div>', unsafe_allow_html=True)


def tab_filemanager():
    st.markdown('<span class="section-tag">file read · file write · processing</span>', unsafe_allow_html=True)
    records = st.session_state.m6_records

    col_in, col_out = st.columns(2, gap="large")
    with col_in:
        st.markdown("**Add File Records**")
        c1,c2,c3,c4 = st.columns([1,2,1.5,1])
        with c1: sid   = st.text_input("ID",    placeholder="ID",   key="fm_sid",   label_visibility="collapsed")
        with c2: sname = st.text_input("Name",  placeholder="Name", key="fm_sname", label_visibility="collapsed")
        with c3: marks = st.number_input("Marks",0,100,step=1,      key="fm_marks", label_visibility="collapsed")
        with c4:
            if st.button("+ Add", key="fm_add"):
                if sid.strip() and sname.strip():
                    records.append({"id":sid.strip(),"name":sname.strip(),"marks":int(marks)})
                    st.session_state.m6_records = records; st.rerun()

        for i, r in enumerate(records):
            r1,r2 = st.columns([5,1])
            with r1: st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:0.8rem;padding:3px 0;color:#3b2007'>[{r['id']}] {r['name']} — {r['marks']} marks</div>", unsafe_allow_html=True)
            with r2:
                if st.button("✕", key=f"fm_del_{i}"):
                    records.pop(i); st.session_state.m6_records=records; st.rerun()
        if not records: st.caption("No records added.")

        st.markdown("**Or load students from registry**")
        if st.button("📥  Import from Registry", key="fm_import"):
            for s in st.session_state.students:
                if not any(r["id"]==s["roll_no"] for r in records):
                    records.append({"id":s["roll_no"],"name":s["name"],"marks":int(s["score"])})
            st.session_state.m6_records = records; st.rerun()

        b1,b2 = st.columns(2)
        with b1: run = st.button("▶  Write & Report", key="fm_run", type="primary")
        with b2:
            if st.button("Clear", key="fm_clear"):
                st.session_state.m6_records=[]; st.rerun()

    with col_out:
        if run:
            if not records: st.error("No records to write.")
            else:
                fname = "student_records.txt"
                with open(fname,"w") as f:
                    f.write("ID, Name, Marks\n")
                    for r in records: f.write(f"{r['id']}, {r['name']}, {r['marks']}\n")
                total = len(records)
                avg   = round(sum(r["marks"] for r in records)/total,1)
                top   = max(records, key=lambda r: r["marks"])
                rows  = "".join(f'<div class="result-row"><span class="result-label">[{r["id"]}] {r["name"]}</span><span class="result-value">{r["marks"]}/100</span></div>' for r in records)
                st.markdown(f"""
                <div class="output-card">
                  <div style="font-family:DM Mono,monospace;font-size:0.62rem;text-transform:uppercase;
                              letter-spacing:0.1em;color:#8b6340;margin-bottom:0.8rem">✔ Written to {fname}</div>
                  {rows}
                  <div style="margin-top:0.8rem;padding-top:0.8rem;border-top:1.5px dashed #c9a978">
                    <div class="result-row"><span class="result-label">Students</span><span class="result-value">{total}</span></div>
                    <div class="result-row"><span class="result-label">Average</span><span class="result-value">{avg}</span></div>
                    <div class="result-row" style="background:#3b2007">
                      <span class="result-label" style="color:#c9a978">Top</span>
                      <span class="result-value" style="color:#f5ede0">{top['name']} · {top['marks']}</span>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
                with open(fname) as f:
                    st.download_button("⬇  Download .txt", f, file_name=fname, mime="text/plain")
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Add records and click Write & Report</span></div>', unsafe_allow_html=True)


def render():
    st.subheader("🔧  System Tools")
    st.markdown("""<div class="info-banner">
      🔧 Admin-only utilities. Normal users don't need these — they're here for
      file I/O demos, directory structure simulation, and backup management.
    </div>""", unsafe_allow_html=True)

    t1, t2 = st.tabs(["📂  Directory Scanner", "🗒  File Manager"])
    with t1: tab_directory()
    with t2: tab_filemanager()

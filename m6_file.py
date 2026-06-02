"""Module 06 — File Handling for Academic Records"""
import streamlit as st, os

RECORDS_FILE = "student_records.txt"

def render():
    st.markdown('<span class="section-tag">file read · file write · processing</span>', unsafe_allow_html=True)
    st.subheader("06 · File Handling for Academic Records")

    if "m6_records" not in st.session_state:
        st.session_state.m6_records = []

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Add Records**")
        c1, c2, c3, c4 = st.columns([1, 2, 1.5, 1])
        with c1: sid   = st.text_input("ID",    placeholder="ID",    key="m6_sid",   label_visibility="collapsed")
        with c2: sname = st.text_input("Name",  placeholder="Name",  key="m6_sname", label_visibility="collapsed")
        with c3: marks = st.number_input("Marks", 0, 100, step=1,    key="m6_marks", label_visibility="collapsed")
        with c4:
            if st.button("+ Add", key="m6_add"):
                if sid.strip() and sname.strip():
                    st.session_state.m6_records.append({"id": sid.strip(), "name": sname.strip(), "marks": int(marks)})
                    st.rerun()

        for i, r in enumerate(st.session_state.m6_records):
            r1, r2 = st.columns([5, 1])
            with r1: st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:0.8rem;padding:3px 0;color:#3b2007'>[{r['id']}] {r['name']} — {r['marks']} marks</div>", unsafe_allow_html=True)
            with r2:
                if st.button("✕", key=f"m6_del_{i}"):
                    st.session_state.m6_records.pop(i); st.rerun()
        if not st.session_state.m6_records: st.caption("No records yet.")

        b1, b2 = st.columns(2)
        with b1: run = st.button("▶  Write & Report", key="m6_run", type="primary")
        with b2:
            if st.button("Clear", key="m6_clear"):
                st.session_state.m6_records = []; st.rerun()

    with col_out:
        st.markdown("**Result**")
        if run:
            recs = st.session_state.m6_records
            if not recs:
                st.error("Add at least one record.")
            else:
                with open(RECORDS_FILE, "w") as f:
                    f.write("ID, Name, Marks\n")
                    for r in recs: f.write(f"{r['id']}, {r['name']}, {r['marks']}\n")

                total = len(recs)
                avg   = round(sum(r["marks"] for r in recs) / total, 1)
                top   = max(recs, key=lambda r: r["marks"])
                rows  = "".join(f'<div class="result-row"><span class="result-label">[{r["id"]}] {r["name"]}</span><span class="result-value">{r["marks"]} / 100</span></div>' for r in recs)

                st.markdown(f"""
                <div class="output-card">
                  <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#8b6340;margin-bottom:0.8rem">✔ Written to {RECORDS_FILE}</div>
                  {rows}
                  <div style="margin-top:1rem;padding-top:0.8rem;border-top:1.5px dashed #c9a978">
                    <div class="result-row"><span class="result-label">Students</span><span class="result-value">{total}</span></div>
                    <div class="result-row"><span class="result-label">Average</span><span class="result-value">{avg} marks</span></div>
                    <div class="result-row" style="background:#3b2007"><span class="result-label" style="color:#c9a978">Top Student</span><span class="result-value" style="color:#f5ede0">{top['name']} · {top['marks']}</span></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                with open(RECORDS_FILE) as f:
                    st.download_button("⬇  Download .txt", f, file_name=RECORDS_FILE, mime="text/plain")
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Add records and click Write & Report</span></div>', unsafe_allow_html=True)

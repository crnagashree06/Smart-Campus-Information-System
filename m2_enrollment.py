"""Module 02 — Course Enrollment Management System (while · for · break · continue)"""
import streamlit as st

def render():
    st.markdown('<span class="section-tag">while · for · break · continue</span>', unsafe_allow_html=True)
    st.subheader("02 · Course Enrollment Management System")

    if "m2_courses" not in st.session_state:
        st.session_state.m2_courses = []

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Input — Add Courses (max 5)**")
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            cname   = st.text_input("Course Name", placeholder="e.g. Data Structures", key="m2_cname", label_visibility="collapsed")
        with c2:
            credits = st.number_input("Cr", min_value=1, max_value=10, step=1, key="m2_credits", label_visibility="collapsed")
        with c3:
            if st.button("+ Add", key="m2_add"):
                if len(st.session_state.m2_courses) >= 5:
                    st.warning("Max 5 courses reached.")
                elif cname.strip():
                    st.session_state.m2_courses.append({"name": cname.strip(), "credits": credits})
                    st.rerun()

        for i, c in enumerate(st.session_state.m2_courses):
            r1, r2 = st.columns([5, 1])
            with r1:
                st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:0.8rem;padding:3px 0;color:#3b2007'>{c['name']} — {c['credits']} credit{'s' if c['credits']>1 else ''}</div>", unsafe_allow_html=True)
            with r2:
                if st.button("✕", key=f"m2_del_{i}"):
                    st.session_state.m2_courses.pop(i); st.rerun()

        if not st.session_state.m2_courses:
            st.caption("No courses added yet.")

        b1, b2 = st.columns(2)
        with b1: run = st.button("▶  Generate Report", key="m2_run", type="primary")
        with b2:
            if st.button("Clear", key="m2_clear"):
                st.session_state.m2_courses = []; st.rerun()

    with col_out:
        st.markdown("**Result**")
        if run:
            courses = st.session_state.m2_courses
            if not courses:
                st.error("No courses added.")
            else:
                total = sum(c["credits"] for c in courses)
                rows  = "".join(
                    f'<div class="result-row">'
                    f'<span class="result-label">{c["name"]}</span>'
                    f'<span class="result-value">{c["credits"]} cr</span></div>'
                    for c in courses
                )
                st.markdown(f"""
                <div class="output-card">
                  <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#8b6340;margin-bottom:0.8rem">Enrollment Report</div>
                  {rows}
                  <div class="result-row" style="margin-top:0.4rem;border-top:2px solid #c9a978;border-radius:0">
                    <span class="result-label">Total</span>
                    <span class="result-value">{len(courses)} courses · {total} credits</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Add courses and click Generate</span></div>', unsafe_allow_html=True)

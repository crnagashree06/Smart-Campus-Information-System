"""Module 03 — Student Record Data Management (list · dict · set)
   Reads directly from st.session_state.students — no re-entry."""
import streamlit as st

def render():
    st.markdown('<span class="section-tag">list · dict · set</span>', unsafe_allow_html=True)
    st.subheader("03 · Student Record Data Management")

    students = st.session_state.students

    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">↖ No students registered yet — go to Module 01 first.</span></div>', unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="info-banner">
      ✔ Loaded <strong>{len(students)}</strong> student{'s' if len(students)!=1 else ''} from the registry.
      Add event participation data below, then run the analysis.
    </div>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Event Participation (Set Analysis)**")
        event_a = st.text_input("Event A participants (comma-separated names)", placeholder="e.g. Priya, Rahul, Anita", key="m3_ea")
        event_b = st.text_input("Event B participants (comma-separated names)", placeholder="e.g. Rahul, Anita, Sneha", key="m3_eb")
        run = st.button("▶  Run Analysis", key="m3_run", type="primary")

        st.markdown("**Registered Students Preview**")
        for s in students:
            avg = round((s["math"] + s["sci"] + s["eng"]) / 3, 1)
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:0.78rem;padding:4px 0;"
                f"border-bottom:1px solid #e8d5b7;color:#3b2007'>"
                f"<span style='color:#8b4513;font-weight:700'>[{s['roll_no']}]</span> "
                f"{s['name']} · Age {s['age']} · Avg {avg}</div>",
                unsafe_allow_html=True,
            )

    with col_out:
        st.markdown("**Result**")
        if run:
            student_rows = ""
            for s in students:
                grades_list = [s["math"], s["sci"], s["eng"]]
                avg = round(sum(grades_list) / 3, 1)
                student_rows += (
                    f'<div class="result-row">'
                    f'<span class="result-label">[{s["roll_no"]}] {s["name"]}</span>'
                    f'<span class="result-value">Age {s["age"]} · Avg {avg}</span>'
                    f'</div>'
                )

            eA = [x.strip() for x in event_a.split(",") if x.strip()]
            eB = [x.strip() for x in event_b.split(",") if x.strip()]
            set_html = ""
            if eA or eB:
                sA, sB = set(eA), set(eB)
                common = sorted(sA & sB)
                only_a = sorted(sA - sB)
                union  = sorted(sA | sB)
                set_html = f"""
                <div style="margin-top:1rem;padding-top:0.8rem;border-top:1.5px dashed #c9a978">
                  <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
                              color:#8b6340;margin-bottom:0.5rem">Set Analysis</div>
                  <div class="result-row">
                    <span class="result-label">Common</span>
                    <span class="result-value">{', '.join(common) or '∅'}</span>
                  </div>
                  <div class="result-row">
                    <span class="result-label">Only A</span>
                    <span class="result-value">{', '.join(only_a) or '∅'}</span>
                  </div>
                  <div class="result-row">
                    <span class="result-label">Union</span>
                    <span class="result-value">{', '.join(union) or '∅'}</span>
                  </div>
                </div>"""

            st.markdown(f"""
            <div class="output-card">
              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;
                          color:#8b6340;margin-bottom:0.8rem">Student Records</div>
              {student_rows}
              {set_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Optionally add event data, then click Run</span></div>', unsafe_allow_html=True)

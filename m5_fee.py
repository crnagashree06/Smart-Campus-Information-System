"""Module 05 — Student Fee Calculation — pick student from registry"""
import streamlit as st

def calculate_fee(tuition, hostel=0.0, transport=0.0):
    return {"tuition": tuition, "hostel": hostel, "transport": transport, "total": tuition+hostel+transport}

def fmt_inr(n):
    return f"₹{n:,.0f}"

def render():
    st.markdown('<span class="section-tag">functions · default params</span>', unsafe_allow_html=True)
    st.subheader("05 · Student Fee Calculation")

    students = st.session_state.students
    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">↖ No students registered yet — go to Module 01 first.</span></div>', unsafe_allow_html=True)
        return

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Input**")
        options = [f'{s["roll_no"]} — {s["name"]}' for s in students]
        selected = st.selectbox("Select Student", options, key="m5_student")
        tuition   = st.number_input("Tuition Fee (₹)",              min_value=0.0, step=500.0, key="m5_tuition")
        hostel    = st.number_input("Hostel Fee (₹, optional)",      min_value=0.0, step=500.0, key="m5_hostel")
        transport = st.number_input("Transportation Fee (₹, optional)", min_value=0.0, step=500.0, key="m5_transport")
        run = st.button("▶  Calculate Fee", key="m5_run", type="primary")

    with col_out:
        st.markdown("**Result**")
        if run:
            if tuition <= 0:
                st.error("Enter a valid tuition fee.")
            else:
                roll_str = selected.split(" — ")[0]
                student  = next(s for s in students if s["roll_no"] == roll_str)
                fee = calculate_fee(tuition, hostel, transport)
                rows = f'<div class="result-row"><span class="result-label">Tuition</span><span class="result-value">{fmt_inr(fee["tuition"])}</span></div>'
                if fee["hostel"] > 0:
                    rows += f'<div class="result-row"><span class="result-label">Hostel</span><span class="result-value">{fmt_inr(fee["hostel"])}</span></div>'
                if fee["transport"] > 0:
                    rows += f'<div class="result-row"><span class="result-label">Transport</span><span class="result-value">{fmt_inr(fee["transport"])}</span></div>'

                st.markdown(f"""
                <div class="output-card">
                  <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;
                              color:#8b6340;margin-bottom:0.8rem">
                    Fee Statement · {student['name']} (Roll {student['roll_no']})
                  </div>
                  {rows}
                  <div class="result-row" style="margin-top:0.6rem;background:#3b2007;border-radius:8px">
                    <span class="result-label" style="color:#c9a978">Total Due</span>
                    <span class="result-value" style="color:#f5ede0;font-size:1.4rem">{fmt_inr(fee["total"])}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Select a student and enter fees</span></div>', unsafe_allow_html=True)

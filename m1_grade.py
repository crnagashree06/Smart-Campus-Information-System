"""
Module 01 — Student Registration & Grade Evaluation
Single entry point. Every other module reads from st.session_state.students.

Each student dict:
  roll_no (str), name (str), age (int),
  score   (float)  — overall exam score used for grade
  math    (float)  — used by Module 08 analytics
  sci     (float)
  eng     (float)
"""
import streamlit as st

GRADE_MAP = [
    (90, "A", "Excellent",         "#6b3a1f"),
    (75, "B", "Very Good",         "#7a4a25"),
    (60, "C", "Good",              "#8b6340"),
    (40, "D", "Average",           "#a07850"),
    ( 0, "F", "Needs Improvement", "#c0392b"),
]

def evaluate_grade(score):
    for threshold, grade, remark, color in GRADE_MAP:
        if score >= threshold:
            return grade, remark, color
    return "F", "Needs Improvement", "#c0392b"


def render():
    st.markdown('<span class="section-tag">if · elif · else · registration hub</span>', unsafe_allow_html=True)
    st.subheader("01 · Student Registration & Grade Evaluation")

    st.markdown("""
    <div class="info-banner">
      📌  Register all students here first. Roll numbers, names, scores and subject marks
      are stored and shared automatically with every other module — no re-entry needed.
    </div>
    """, unsafe_allow_html=True)

    students = st.session_state.students

    # ── Registration form ────────────────────────────────────────────────────
    with st.expander("➕  Add a New Student", expanded=len(students) == 0):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            roll = st.text_input("Roll No.", placeholder="e.g. 101", key="m1_roll")
        with c2:
            name = st.text_input("Full Name", placeholder="e.g. Priya Sharma", key="m1_name")
        with c3:
            age  = st.number_input("Age", min_value=16, max_value=30, step=1, value=18, key="m1_age")

        st.markdown("**Exam & Subject Scores** (0 – 100)")
        s1, s2, s3, s4 = st.columns(4)
        with s1: score = st.number_input("Overall Score", 0.0, 100.0, step=0.5, key="m1_score")
        with s2: math  = st.number_input("Mathematics",   0.0, 100.0, step=0.5, key="m1_math")
        with s3: sci   = st.number_input("Science",       0.0, 100.0, step=0.5, key="m1_sci")
        with s4: eng   = st.number_input("English",       0.0, 100.0, step=0.5, key="m1_eng")

        b1, b2 = st.columns([1, 4])
        with b1:
            add_btn = st.button("✚  Register Student", key="m1_add", type="primary")

        if add_btn:
            if not roll.strip():
                st.error("Roll number is required.")
            elif not name.strip():
                st.error("Student name is required.")
            elif any(s["roll_no"] == roll.strip() for s in students):
                st.error(f"Roll No. {roll.strip()} is already registered.")
            else:
                students.append({
                    "roll_no": roll.strip(),
                    "name":    name.strip(),
                    "age":     int(age),
                    "score":   float(score),
                    "math":    float(math),
                    "sci":     float(sci),
                    "eng":     float(eng),
                })
                st.session_state.students = students
                st.success(f"✔  {name.strip()} (Roll {roll.strip()}) registered successfully!")
                st.rerun()

    st.markdown("---")

    # ── Registered students table + grade evaluation ─────────────────────────
    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">No students registered yet — use the form above.</span></div>', unsafe_allow_html=True)
        return

    st.markdown(f"**Registered Students — Grade Report** &nbsp; `{len(students)} student{'s' if len(students)!=1 else ''}`")

    # Header row
    header = """
    <div style="display:grid;grid-template-columns:80px 1fr 60px 80px 80px 80px 80px 80px 120px;
                gap:0.5rem;padding:0.5rem 1rem;background:#3b2007;border-radius:8px 8px 0 0;
                font-family:DM Mono,monospace;font-size:0.65rem;letter-spacing:0.1em;
                text-transform:uppercase;color:#c9a978;margin-top:0.5rem">
      <div>Roll No.</div><div>Name</div><div>Age</div>
      <div>Score</div><div>Math</div><div>Sci</div><div>Eng</div>
      <div>Grade</div><div>Remark</div>
    </div>"""
    st.markdown(header, unsafe_allow_html=True)

    rows_html = ""
    for i, s in enumerate(students):
        grade, remark, col = evaluate_grade(s["score"])
        bg = "#fdf6ec" if i % 2 == 0 else "#f5e6ce"
        rows_html += f"""
        <div style="display:grid;grid-template-columns:80px 1fr 60px 80px 80px 80px 80px 80px 120px;
                    gap:0.5rem;padding:0.55rem 1rem;background:{bg};
                    font-family:DM Mono,monospace;font-size:0.78rem;color:#2c1a0e;
                    border-left:1px solid #e0c9a8;border-right:1px solid #e0c9a8;
                    border-bottom:1px solid #e8d5b7">
          <div style="color:#8b4513;font-weight:700">{s['roll_no']}</div>
          <div style="font-family:Lato,sans-serif;font-weight:600">{s['name']}</div>
          <div>{s['age']}</div>
          <div>{s['score']}</div>
          <div>{s['math']}</div>
          <div>{s['sci']}</div>
          <div>{s['eng']}</div>
          <div style="color:{col};font-weight:700;font-size:1rem">{grade}</div>
          <div style="color:{col};font-size:0.72rem">{remark}</div>
        </div>"""

    st.markdown(rows_html, unsafe_allow_html=True)

    # Summary bar
    avg_score = round(sum(s["score"] for s in students) / len(students), 1)
    top = max(students, key=lambda s: s["score"])
    st.markdown(f"""
    <div style="display:flex;gap:1.5rem;flex-wrap:wrap;padding:0.7rem 1rem;
                background:#3b2007;border-radius:0 0 8px 8px;margin-bottom:1rem">
      <span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">
        Class Average: <strong style="color:#f5ede0">{avg_score}</strong>
      </span>
      <span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">
        Top Student: <strong style="color:#f5ede0">{top['name']}</strong> ({top['score']})
      </span>
      <span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">
        Total: <strong style="color:#f5ede0">{len(students)}</strong>
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Remove a student
    with st.expander("🗑  Remove a Student"):
        roll_to_remove = st.selectbox(
            "Select student to remove",
            options=[f"{s['roll_no']} — {s['name']}" for s in students],
            key="m1_remove_sel"
        )
        if st.button("Remove Selected", key="m1_remove_btn"):
            roll_key = roll_to_remove.split(" — ")[0]
            st.session_state.students = [s for s in students if s["roll_no"] != roll_key]
            st.rerun()

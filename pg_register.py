"""
Register Student — two-step flow:
  Step 1 (Course Setup tab): define courses + credits
  Step 2 (Register Student tab): enter marks per course, auto-calculates weighted %
"""
import streamlit as st

GRADE_MAP = [
    (90, "A", "Excellent",         "#557a3a"),
    (75, "B", "Very Good",         "#3a6b7a"),
    (60, "C", "Good",              "#7a6b3a"),
    (40, "D", "Average",           "#7a5030"),
    ( 0, "F", "Needs Improvement", "#8b2020"),
]

def evaluate_grade(score):
    for threshold, grade, remark, color in GRADE_MAP:
        if score >= threshold:
            return grade, remark, color
    return "F", "Needs Improvement", "#8b2020"

def calc_weighted_percentage(courses, marks):
    """Weighted % = sum(mark * credits) / sum(all credits)"""
    total_credits = sum(c["credits"] for c in courses)
    if total_credits == 0:
        return 0.0
    weighted_sum = sum(marks.get(c["name"], 0) * c["credits"] for c in courses)
    return round(weighted_sum / total_credits, 2)


# ── Tab 1 — Course Setup (initialization) ────────────────────────────────────
def tab_course_setup():
    st.markdown("""<div class="info-banner">
      📐 <strong>Step 1 — Initialize Courses.</strong> Define all courses and their credit values first.
      These will appear as mark-entry fields when you register each student.
    </div>""", unsafe_allow_html=True)

    courses = st.session_state.courses

    # ── Add course form ───────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        cname = st.text_input(
            "Course Name", placeholder="e.g. Mathematics",
            key="cs_name", label_visibility="collapsed"
        )
    with c2:
        credits = st.number_input(
            "Credits", min_value=1, max_value=10, step=1,
            key="cs_credits", label_visibility="collapsed"
        )
    with c3:
        add = st.button("+ Add Course", key="cs_add", type="primary")

    if add:
        if not cname.strip():
            st.warning("Enter a course name.")
        elif any(c["name"].lower() == cname.strip().lower() for c in courses):
            st.warning("That course already exists.")
        else:
            courses.append({"name": cname.strip(), "credits": int(credits)})
            st.session_state.courses = courses
            st.rerun()

    # ── Current courses list ──────────────────────────────────────────────────
    if courses:
        total_credits = sum(c["credits"] for c in courses)

        st.markdown("**Initialized Courses**")

        header = (
            '<div style="display:grid;grid-template-columns:1fr 80px 80px;gap:0.4rem;'
            'padding:0.5rem 1rem;background:#3b2007;border-radius:8px 8px 0 0;'
            'font-family:DM Mono,monospace;font-size:0.63rem;letter-spacing:0.1em;'
            'text-transform:uppercase;color:#c9a978">'
            '<div>Course</div><div>Credits</div><div>Remove</div></div>'
        )
        st.markdown(header, unsafe_allow_html=True)

        for i, c in enumerate(courses):
            bg = "#fdf6ec" if i % 2 == 0 else "#f5e6ce"
            col_a, col_b, col_c = st.columns([5, 1, 1])
            with col_a:
                st.markdown(
                    '<div style="background:' + bg + ';padding:0.5rem 1rem;'
                    'font-family:Lato,sans-serif;font-size:0.85rem;color:#2c1a0e;'
                    'border:1px solid #e8d5b7;border-top:none">'
                    + c["name"] + '</div>',
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    '<div style="background:' + bg + ';padding:0.5rem 0.5rem;'
                    'font-family:DM Mono,monospace;font-size:0.82rem;color:#6b3a1f;'
                    'border:1px solid #e8d5b7;border-top:none;border-left:none;text-align:center">'
                    + str(c["credits"]) + ' cr</div>',
                    unsafe_allow_html=True
                )
            with col_c:
                if st.button("✕", key="cs_del_" + str(i)):
                    courses.pop(i)
                    st.session_state.courses = courses
                    st.rerun()

        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 80px 80px;gap:0.4rem;'
            'padding:0.5rem 1rem;background:#3b2007;border-radius:0 0 8px 8px;'
            'font-family:DM Mono,monospace;font-size:0.72rem;color:#c9a978;margin-bottom:1rem">'
            '<div style="text-align:right;padding-right:0.5rem">Total</div>'
            '<div style="font-weight:700">' + str(total_credits) + ' cr</div>'
            '<div></div></div>',
            unsafe_allow_html=True
        )

        if st.button("🗑  Clear All Courses", key="cs_clear"):
            st.session_state.courses = []
            st.rerun()

        st.success("✔ " + str(len(courses)) + " course(s) initialized — go to **Register Student** tab to enroll students.")
    else:
        st.markdown(
            '<div class="output-card"><span class="output-placeholder">'
            'No courses yet — add courses above to get started.'
            '</span></div>',
            unsafe_allow_html=True
        )


# ── Tab 2 — Register Student ──────────────────────────────────────────────────
def tab_register():
    courses  = st.session_state.courses
    students = st.session_state.students

    # Guard: courses must be set up first
    if not courses:
        st.markdown("""<div class="warn-banner">
          ⚠ <strong>No courses initialized yet.</strong>
          Go to the <strong>Course Setup</strong> tab first and add your courses + credits.
          The mark-entry fields will appear here once courses are set up.
        </div>""", unsafe_allow_html=True)
        return

    st.markdown("""<div class="info-banner">
      📝 <strong>Step 2 — Register Student.</strong>
      Enter student details and marks for each initialized course.
      Overall percentage is calculated automatically using weighted credits.
    </div>""", unsafe_allow_html=True)

    # Show initialized courses as a reference pill row
    pills = "".join(
        '<span style="background:#e8d0b0;color:#6b3a1f;font-family:DM Mono,monospace;'
        'font-size:0.68rem;padding:2px 10px;border-radius:12px;margin-right:6px;'
        'border-left:3px solid #8b4513">' + c["name"] + ' · ' + str(c["credits"]) + 'cr</span>'
        for c in courses
    )
    st.markdown(
        '<div style="margin-bottom:1rem;line-height:2.2">Courses: ' + pills + '</div>',
        unsafe_allow_html=True
    )

    with st.expander("➕  Add New Student", expanded=len(students) == 0):

        # ── Basic info ────────────────────────────────────────────────────────
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1: roll = st.text_input("Roll No.", placeholder="e.g. 101", key="reg_roll")
        with c2: name = st.text_input("Full Name", placeholder="e.g. Priya Sharma", key="reg_name")
        with c3: age  = st.number_input("Age", 16, 30, value=18, key="reg_age")

        # ── Marks — one field per initialized course ──────────────────────────
        st.markdown("**Marks for Each Course** (0 – 100)")

        marks = {}
        # Display in rows of 3
        for row_start in range(0, len(courses), 3):
            row_courses = courses[row_start: row_start + 3]
            cols = st.columns(len(row_courses))
            for col, course in zip(cols, row_courses):
                with col:
                    val = st.number_input(
                        course["name"] + " (" + str(course["credits"]) + " cr)",
                        min_value=0.0, max_value=100.0, step=0.5,
                        key="reg_mark_" + course["name"]
                    )
                    marks[course["name"]] = float(val)

        # ── Live weighted % preview ───────────────────────────────────────────
        pct = calc_weighted_percentage(courses, marks)
        grade, remark, gcol = evaluate_grade(pct)
        total_credits = sum(c["credits"] for c in courses)

        preview_rows = "".join(
            '<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.3rem">'
            '<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#8b6340;min-width:140px">'
            + c["name"] + '</span>'
            '<div style="flex:1;background:#e8d0b0;border-radius:3px;height:8px;overflow:hidden">'
            '<div style="width:' + str(marks.get(c["name"], 0)) + '%;background:#8b4513;height:100%;border-radius:3px"></div>'
            '</div>'
            '<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#3b2007;min-width:45px;text-align:right">'
            + str(marks.get(c["name"], 0)) + '</span>'
            '</div>'
            for c in courses
        )

        st.markdown(
            '<div style="background:#fdf6ec;border:1.5px solid #c9a978;border-radius:12px;'
            'padding:1rem 1.2rem;margin-top:0.8rem">'
            '<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:0.1em;'
            'text-transform:uppercase;color:#8b6340;margin-bottom:0.6rem">Live Score Preview</div>'
            + preview_rows +
            '<div style="display:flex;align-items:center;gap:1.5rem;margin-top:0.8rem;'
            'padding-top:0.8rem;border-top:1.5px dashed #c9a978">'
            '<div style="font-family:DM Mono,monospace;font-size:0.7rem;color:#8b6340">'
            'Total Credits: <strong style="color:#3b2007">' + str(total_credits) + '</strong></div>'
            '<div style="font-family:DM Mono,monospace;font-size:0.7rem;color:#8b6340">'
            'Weighted %: <strong style="color:#3b2007;font-size:1.15rem">' + str(pct) + '%</strong></div>'
            '<div style="font-family:Playfair Display,serif;font-size:1.3rem;'
            'font-weight:700;color:' + gcol + '">' + grade + '</div>'
            '<div style="font-family:DM Mono,monospace;font-size:0.72rem;color:' + gcol + '">'
            + remark + '</div>'
            '</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("")
        if st.button("✚  Register Student", key="reg_add", type="primary"):
            if not roll.strip():
                st.error("Roll number is required.")
            elif not name.strip():
                st.error("Student name is required.")
            elif any(s["roll_no"] == roll.strip() for s in students):
                st.error("Roll No. " + roll.strip() + " already exists.")
            else:
                pct = calc_weighted_percentage(courses, marks)
                students.append({
                    "roll_no":  roll.strip(),
                    "name":     name.strip(),
                    "age":      int(age),
                    "subjects": marks.copy(),
                    "score":    pct,
                    # legacy fields for analytics
                    "math": marks.get("Mathematics", marks.get("Math", marks.get("Physics", 0.0))),
                    "sci":  marks.get("Science",     marks.get("Chemistry", marks.get("Biology", 0.0))),
                    "eng":  marks.get("English",     0.0),
                })
                st.session_state.students = students
                st.success("✔ " + name.strip() + " registered — Weighted %: " + str(pct))
                st.rerun()

    # ── Registered students table ─────────────────────────────────────────────
    if not students:
        st.markdown(
            '<div class="output-card" style="margin-top:1rem">'
            '<span class="output-placeholder">No students registered yet — use the form above.</span>'
            '</div>',
            unsafe_allow_html=True
        )
        return

    st.markdown("---")
    n      = len(students)
    suffix = "s" if n != 1 else ""
    st.markdown("**Grade Report** &nbsp;`" + str(n) + " student" + suffix + " registered`")

    col_def = "80px 1fr 50px 90px 80px 130px"
    st.markdown(
        '<div style="display:grid;grid-template-columns:' + col_def + ';gap:0.4rem;'
        'padding:0.5rem 1rem;background:#3b2007;border-radius:8px 8px 0 0;'
        'font-family:DM Mono,monospace;font-size:0.63rem;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#c9a978;margin-top:0.4rem">'
        '<div>Roll</div><div>Name</div><div>Age</div>'
        '<div>Weighted %</div><div>Grade</div><div>Remark</div>'
        '</div>',
        unsafe_allow_html=True
    )

    rows_html = ""
    for i, s in enumerate(students):
        grade, remark, col = evaluate_grade(s["score"])
        bg = "#fdf6ec" if i % 2 == 0 else "#f5e6ce"
        rows_html += (
            '<div style="display:grid;grid-template-columns:' + col_def + ';gap:0.4rem;'
            'padding:0.55rem 1rem;background:' + bg + ';'
            'font-family:DM Mono,monospace;font-size:0.76rem;color:#2c1a0e;'
            'border:1px solid #e8d5b7;border-top:none">'
            '<div style="color:#8b4513;font-weight:700">' + s["roll_no"] + '</div>'
            '<div style="font-family:Lato,sans-serif;font-weight:600">' + s["name"] + '</div>'
            '<div>' + str(s["age"]) + '</div>'
            '<div style="font-weight:700;color:#3b2007">' + str(s["score"]) + '%</div>'
            '<div style="color:' + col + ';font-weight:700;font-size:0.95rem">' + grade + '</div>'
            '<div style="color:' + col + ';font-size:0.7rem">' + remark + '</div>'
            '</div>'
        )
    st.markdown(rows_html, unsafe_allow_html=True)

    avg  = round(sum(s["score"] for s in students) / len(students), 1)
    top  = max(students, key=lambda s: s["score"])
    st.markdown(
        '<div style="display:flex;gap:2rem;flex-wrap:wrap;padding:0.65rem 1rem;'
        'background:#3b2007;border-radius:0 0 8px 8px;margin-bottom:1.2rem">'
        '<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">'
        'Class Avg: <strong style="color:#f5ede0">' + str(avg) + '%</strong></span>'
        '<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">'
        'Top: <strong style="color:#f5ede0">' + top["name"] + '</strong> (' + str(top["score"]) + '%)</span>'
        '<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a978">'
        'Total: <strong style="color:#f5ede0">' + str(len(students)) + '</strong></span>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander("🗑  Remove a Student"):
        options = [s["roll_no"] + " — " + s["name"] for s in students]
        sel = st.selectbox("Select", options, key="reg_rm_sel")
        if st.button("Remove", key="reg_rm_btn"):
            rk = sel.split(" — ")[0]
            st.session_state.students = [s for s in students if s["roll_no"] != rk]
            st.rerun()


# ── Main render ───────────────────────────────────────────────────────────────
def render():
    st.subheader("📝  Register Student")
    t1, t2 = st.tabs(["📐  Course Setup", "🧑‍🎓  Register Student"])
    with t1: tab_course_setup()
    with t2: tab_register()

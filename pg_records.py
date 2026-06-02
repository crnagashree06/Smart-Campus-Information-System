"""Student Records — 3 sub-tabs: View & Display · Search & Sort · Fee Calculator"""
import streamlit as st

def roll_key(s):
    try:    return int(s["roll_no"])
    except: return s["roll_no"]

def fmt_inr(n):
    return "₹" + "{:,.0f}".format(n)

def bubble_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]
    return a

def selection_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]: m = j
        a[i], a[m] = a[m], a[i]
    return a

def linear_search(arr, t):
    for i, v in enumerate(arr):
        if v == t: return i
    return -1

def binary_search(arr, t):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == t:   return mid
        elif arr[mid] < t:  lo = mid + 1
        else:               hi = mid - 1
    return -1


# ── Tab 1 — View & Display ────────────────────────────────────────────────────
def tab_display(students):
    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">No students registered — go to Register Student first.</span></div>', unsafe_allow_html=True)
        return

    from modules.pg_register import evaluate_grade

    c1, c2 = st.columns([2, 2])
    with c1:
        search_name = st.text_input("🔎 Filter by name", placeholder="e.g. Pri", key="disp_filter")
    with c2:
        sort_by = st.selectbox("Sort by", ["Roll No.", "Name", "Overall %"], key="disp_sort")

    filtered = [s for s in students if search_name.lower() in s["name"].lower()] if search_name else students[:]
    key_map  = {
        "Roll No.": roll_key,
        "Name":     lambda s: s["name"],
        "Overall %": lambda s: -s["score"],
    }
    filtered.sort(key=key_map[sort_by])

    n = len(filtered)
    suffix = "s" if n != 1 else ""
    st.markdown(
        '<div style="font-family:DM Mono,monospace;font-size:0.7rem;color:#8b6340;margin-bottom:0.5rem">'
        + str(n) + " student" + suffix + " shown</div>",
        unsafe_allow_html=True
    )

    col_def = "80px 1fr 50px 150px 80px 80px 120px"
    st.markdown(
        '<div style="display:grid;grid-template-columns:' + col_def + ';gap:0.4rem;'
        'padding:0.5rem 1rem;background:#3b2007;border-radius:8px 8px 0 0;'
        'font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#c9a978;margin-top:0.4rem">'
        '<div>Roll</div><div>Name</div><div>Age</div>'
        '<div>Subjects</div><div>Overall %</div><div>Grade</div><div>Remark</div>'
        '</div>',
        unsafe_allow_html=True
    )

    rows = ""
    for i, s in enumerate(filtered):
        grade, remark, col = evaluate_grade(s["score"])
        bg        = "#fdf6ec" if i % 2 == 0 else "#f5e6ce"
        subj_list = ", ".join(s.get("subjects", {}).keys()) or "—"
        rows += (
            '<div style="display:grid;grid-template-columns:' + col_def + ';gap:0.4rem;'
            'padding:0.5rem 1rem;background:' + bg + ';'
            'font-family:DM Mono,monospace;font-size:0.76rem;color:#2c1a0e;'
            'border:1px solid #e8d5b7;border-top:none">'
            '<div style="color:#8b4513;font-weight:700">' + s["roll_no"] + '</div>'
            '<div style="font-family:Lato,sans-serif;font-weight:600">' + s["name"] + '</div>'
            '<div>' + str(s["age"]) + '</div>'
            '<div style="font-size:0.68rem;color:#6b3a1f">' + subj_list + '</div>'
            '<div style="font-weight:700">' + str(s["score"]) + '%</div>'
            '<div style="color:' + col + ';font-weight:700">' + grade + '</div>'
            '<div style="color:' + col + ';font-size:0.7rem">' + remark + '</div>'
            '</div>'
        )
    st.markdown(rows, unsafe_allow_html=True)
    st.markdown('<div style="height:8px;background:#3b2007;border-radius:0 0 8px 8px"></div>', unsafe_allow_html=True)

    # Per-student subject breakdown
    st.markdown("---")
    st.markdown("**Subject-wise Marks Breakdown**")
    for s in filtered:
        subjects = s.get("subjects", {})
        if not subjects:
            continue
        marks_html = "".join(
            '<div class="result-row">'
            '<span class="result-label">' + subj + '</span>'
            '<span class="result-value">' + str(mark) + ' / 100</span>'
            '<div style="flex:1;background:#e8d0b0;border-radius:3px;height:8px;overflow:hidden;margin-left:0.5rem">'
            '<div style="width:' + str(mark) + '%;background:#8b4513;height:100%;border-radius:3px"></div>'
            '</div></div>'
            for subj, mark in subjects.items()
        )
        with st.expander(s["roll_no"] + " — " + s["name"] + "  (" + str(s["score"]) + "%)"):
            st.markdown(marks_html, unsafe_allow_html=True)


# ── Tab 2 — Search & Sort ─────────────────────────────────────────────────────
def tab_search(students):
    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">No students registered — go to Register Student first.</span></div>', unsafe_allow_html=True)
        return

    roll_nums = [roll_key(s) for s in students]
    name_of   = {roll_key(s): s["name"] for s in students}

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        algo = st.selectbox("Sort Algorithm",
            ["Both (Bubble + Selection)", "Bubble Sort", "Selection Sort"], key="ss_algo")
        options    = ["(skip search)"] + [s["roll_no"] + " — " + s["name"] for s in students]
        target_sel = st.selectbox("Search for student", options, key="ss_target")
        run        = st.button("▶  Sort & Search", key="ss_run", type="primary")

        roll_pills = "  ·  ".join(
            '<span style="color:#8b4513;font-weight:700">' + s["roll_no"] + '</span> ' + s["name"]
            for s in students
        )
        st.markdown(
            '<div style="font-family:DM Mono,monospace;font-size:0.78rem;'
            'line-height:2;margin-top:0.8rem">' + roll_pills + '</div>',
            unsafe_allow_html=True
        )

    with col_out:
        if run:
            sort_html = ""
            sorted_r  = roll_nums[:]

            def sorted_labels(arr):
                return " → ".join(str(r) + " (" + name_of[r] + ")" for r in arr)

            if "Bubble" in algo or "Both" in algo:
                bs = bubble_sort(roll_nums)
                sort_html += (
                    '<div class="result-row"><span class="result-label">Bubble Sort</span>'
                    '<span class="result-value" style="font-size:0.8rem">' + str(bs) + '</span></div>'
                    '<div style="font-family:DM Mono,monospace;font-size:0.68rem;color:#8b6340;'
                    'padding:2px 1rem 8px">' + sorted_labels(bs) + '</div>'
                )
                sorted_r = bs

            if "Selection" in algo or "Both" in algo:
                ss = selection_sort(roll_nums)
                sort_html += (
                    '<div class="result-row"><span class="result-label">Selection</span>'
                    '<span class="result-value" style="font-size:0.8rem">' + str(ss) + '</span></div>'
                    '<div style="font-family:DM Mono,monospace;font-size:0.68rem;color:#8b6340;'
                    'padding:2px 1rem 8px">' + sorted_labels(ss) + '</div>'
                )
                sorted_r = ss

            search_html = ""
            if target_sel != "(skip search)":
                t_roll_str = target_sel.split(" — ")[0]
                t_name     = target_sel.split(" — ")[1]
                try:    t = int(t_roll_str)
                except: t = t_roll_str
                li = linear_search(sorted_r, t)
                bi = binary_search(sorted_r, t)
                li_txt = "Found at index " + str(li) if li != -1 else "Not found"
                bi_txt = "Found at index " + str(bi) if bi != -1 else "Not found"
                search_html = (
                    '<div style="margin-top:1rem;padding-top:0.8rem;border-top:1.5px dashed #c9a978">'
                    '<div style="font-family:DM Mono,monospace;font-size:0.62rem;text-transform:uppercase;'
                    'letter-spacing:0.1em;color:#8b6340;margin-bottom:0.4rem">'
                    'Searching · ' + t_name + ' (Roll ' + t_roll_str + ')</div>'
                    '<div class="result-row"><span class="result-label">Linear</span>'
                    '<span class="result-value">' + li_txt + '</span></div>'
                    '<div class="result-row"><span class="result-label">Binary</span>'
                    '<span class="result-value">' + bi_txt + '</span></div>'
                    '</div>'
                )

            st.markdown(
                '<div class="output-card">'
                '<div style="font-family:DM Mono,monospace;font-size:0.62rem;text-transform:uppercase;'
                'letter-spacing:0.1em;color:#8b6340;margin-bottom:0.8rem">'
                'Original order: ' + str(roll_nums) + '</div>'
                + sort_html + search_html +
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Choose options and click Sort & Search</span></div>', unsafe_allow_html=True)


# ── Tab 3 — Fee Calculator ────────────────────────────────────────────────────
def tab_fee(students):
    st.markdown('<span class="section-tag">functions · default params</span>', unsafe_allow_html=True)
    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">No students registered yet.</span></div>', unsafe_allow_html=True)
        return

    col_in, col_out = st.columns(2, gap="large")
    with col_in:
        sel       = st.selectbox("Select Student",
            [s["roll_no"] + " — " + s["name"] for s in students], key="fee_sel")
        tuition   = st.number_input("Tuition Fee (₹)",    0.0, step=500.0, key="fee_tuition")
        hostel    = st.number_input("Hostel Fee (₹)",     0.0, step=500.0, key="fee_hostel")
        transport = st.number_input("Transport Fee (₹)",  0.0, step=500.0, key="fee_transport")
        run = st.button("▶  Calculate", key="fee_run", type="primary")

    with col_out:
        if run:
            if tuition <= 0:
                st.error("Enter a valid tuition fee.")
            else:
                roll_str = sel.split(" — ")[0]
                student  = next(s for s in students if s["roll_no"] == roll_str)
                total    = tuition + hostel + transport

                rows = (
                    '<div class="result-row"><span class="result-label">Tuition</span>'
                    '<span class="result-value">' + fmt_inr(tuition) + '</span></div>'
                )
                if hostel > 0:
                    rows += (
                        '<div class="result-row"><span class="result-label">Hostel</span>'
                        '<span class="result-value">' + fmt_inr(hostel) + '</span></div>'
                    )
                if transport > 0:
                    rows += (
                        '<div class="result-row"><span class="result-label">Transport</span>'
                        '<span class="result-value">' + fmt_inr(transport) + '</span></div>'
                    )

                st.markdown(
                    '<div class="output-card">'
                    '<div style="font-family:DM Mono,monospace;font-size:0.62rem;text-transform:uppercase;'
                    'letter-spacing:0.1em;color:#8b6340;margin-bottom:0.8rem">'
                    'Fee Statement · ' + student["name"] + ' (Roll ' + student["roll_no"] + ')</div>'
                    + rows +
                    '<div class="result-row" style="background:#3b2007;border-radius:8px;margin-top:0.6rem">'
                    '<span class="result-label" style="color:#c9a978">Total Due</span>'
                    '<span class="result-value" style="color:#f5ede0;font-size:1.4rem">'
                    + fmt_inr(total) + '</span></div>'
                    '</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Select a student and enter fees</span></div>', unsafe_allow_html=True)


# ── Main render ───────────────────────────────────────────────────────────────
def render():
    st.subheader("🗂  Student Records")
    students = st.session_state.students
    t1, t2, t3 = st.tabs(["📋  View & Display", "🔍  Search & Sort", "💰  Fee Calculator"])
    with t1: tab_display(students)
    with t2: tab_search(students)
    with t3: tab_fee(students)

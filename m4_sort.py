"""Module 04 — Sorting and Searching of Student Roll Numbers
   Roll numbers come from st.session_state.students — no manual entry."""
import streamlit as st

def bubble_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        for j in range(len(a)-i-1):
            if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]
    return a

def selection_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        m = i
        for j in range(i+1, len(a)):
            if a[j] < a[m]: m = j
        a[i], a[m] = a[m], a[i]
    return a

def linear_search(arr, t):
    for i, v in enumerate(arr):
        if v == t: return i
    return -1

def binary_search(arr, t):
    lo, hi = 0, len(arr)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if arr[mid] == t: return mid
        elif arr[mid] < t: lo = mid+1
        else: hi = mid-1
    return -1

def render():
    st.markdown('<span class="section-tag">bubble sort · selection sort · linear · binary</span>', unsafe_allow_html=True)
    st.subheader("04 · Sorting and Searching of Student Roll Numbers")

    students = st.session_state.students

    if not students:
        st.markdown('<div class="output-card"><span class="output-placeholder">↖ No students registered yet — go to Module 01 first.</span></div>', unsafe_allow_html=True)
        return

    # Extract roll numbers (try numeric, fall back to string comparison)
    def roll_key(s):
        try:    return int(s["roll_no"])
        except: return s["roll_no"]

    roll_numbers = [roll_key(s) for s in students]
    roll_display = {roll_key(s): f'{s["roll_no"]} ({s["name"]})' for s in students}

    st.markdown(f"""
    <div class="info-banner">
      ✔ Using roll numbers from <strong>{len(students)}</strong> registered students.
      Pick an algorithm and a target to search.
    </div>
    """, unsafe_allow_html=True)

    # Current roll number list
    st.markdown("**Current Roll Numbers**")
    rolls_str = "  ·  ".join(f'<span style="color:#8b4513;font-weight:700">{s["roll_no"]}</span> {s["name"]}' for s in students)
    st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:0.8rem;line-height:2;padding:0.5rem 0'>{rolls_str}</div>", unsafe_allow_html=True)
    st.markdown("---")

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Search & Sort Options**")
        algo = st.selectbox("Sort Algorithm", ["Both (Bubble + Selection)", "Bubble Sort", "Selection Sort"], key="m4_algo")

        # Search target — pick from registered students
        options = ["(skip search)"] + [f'{s["roll_no"]} — {s["name"]}' for s in students]
        target_sel = st.selectbox("Search for student", options, key="m4_target_sel")
        run = st.button("▶  Sort & Search", key="m4_run", type="primary")

    with col_out:
        st.markdown("**Result**")
        if run:
            sort_html = ""
            sorted_rolls = roll_numbers[:]

            if "Bubble" in algo or "Both" in algo:
                bs = bubble_sort(roll_numbers)
                bs_names = [f'{r} ({next(s["name"] for s in students if roll_key(s)==r)})' for r in bs]
                sort_html += (
                    f'<div class="result-row">'
                    f'<span class="result-label">Bubble Sort</span>'
                    f'<span class="result-value" style="font-size:0.8rem">{bs}</span>'
                    f'</div>'
                    f'<div style="font-family:DM Mono,monospace;font-size:0.7rem;'
                    f'color:#8b6340;padding:4px 1rem 8px">{" → ".join(bs_names)}</div>'
                )
                sorted_rolls = bs

            if "Selection" in algo or "Both" in algo:
                ss = selection_sort(roll_numbers)
                ss_names = [f'{r} ({next(s["name"] for s in students if roll_key(s)==r)})' for r in ss]
                sort_html += (
                    f'<div class="result-row">'
                    f'<span class="result-label">Selection</span>'
                    f'<span class="result-value" style="font-size:0.8rem">{ss}</span>'
                    f'</div>'
                    f'<div style="font-family:DM Mono,monospace;font-size:0.7rem;'
                    f'color:#8b6340;padding:4px 1rem 8px">{" → ".join(ss_names)}</div>'
                )
                sorted_rolls = ss

            search_html = ""
            if target_sel != "(skip search)":
                t_roll_str = target_sel.split(" — ")[0]
                try:    t = int(t_roll_str)
                except: t = t_roll_str
                t_name = target_sel.split(" — ")[1]
                li = linear_search(sorted_rolls, t)
                bi = binary_search(sorted_rolls, t)
                li_txt = f"Found at index {li}" if li != -1 else "Not found"
                bi_txt = f"Found at index {bi}" if bi != -1 else "Not found"
                search_html = f"""
                <div style="margin-top:1rem;padding-top:0.8rem;border-top:1.5px dashed #c9a978">
                  <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
                              color:#8b6340;margin-bottom:0.5rem">Searching · {t_name} (Roll {t_roll_str})</div>
                  <div class="result-row">
                    <span class="result-label">Linear</span>
                    <span class="result-value">{li_txt}</span>
                  </div>
                  <div class="result-row">
                    <span class="result-label">Binary</span>
                    <span class="result-value">{bi_txt}</span>
                  </div>
                </div>"""

            st.markdown(f"""
            <div class="output-card">
              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;
                          color:#8b6340;margin-bottom:0.8rem">Original order: {roll_numbers}</div>
              {sort_html}
              {search_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Choose options and click Sort & Search</span></div>', unsafe_allow_html=True)

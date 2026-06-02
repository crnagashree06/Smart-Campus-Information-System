"""Analytics Dashboard — fully dynamic, reads courses from student subjects directly"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib, matplotlib.pyplot as plt
matplotlib.use("Agg")

from modules.pg_register import evaluate_grade
def render():
    st.subheader("📊  Analytics Dashboard")
    students = st.session_state.students

    # ── ADD THIS TEMPORARILY ──
    if students:
        st.write("DEBUG:", students[0])
    # ─────────────────────────
render()
BROWN_PALETTE = [
    "#6b3a1f","#8b4513","#a0522d","#c9a978",
    "#5c3317","#3b2007","#d4956a","#e8c49a",
    "#4a2810","#b07840",
]

def style_fig(fig, axes=None):
    fig.patch.set_facecolor("#fdf6ec")
    for ax in (axes or fig.axes):
        ax.set_facecolor("#fdf6ec")
        ax.tick_params(colors="#5a3e2b", labelsize=8)
        for sp in ax.spines.values():
            sp.set_edgecolor("#c9a97855")

def no_data_card(msg="No students registered — go to Register Student first."):
    st.markdown(
        '<div class="output-card"><span class="output-placeholder">' + msg + '</span></div>',
        unsafe_allow_html=True
    )

def get_course_names(students):
    """
    Get course names in this priority order:
    1. From st.session_state.courses (if courses were initialized)
    2. Directly from students' subjects dicts (fallback — always works)
    This ensures analytics works even if session state was partially reset.
    """
    if st.session_state.get("courses"):
        return [c["name"] for c in st.session_state.courses]
    # Fallback: collect all unique subject keys from every student
    seen = []
    for s in students:
        for key in s.get("subjects", {}).keys():
            if key not in seen:
                seen.append(key)
    return seen

def student_mark(student, course_name):
    return float(student.get("subjects", {}).get(course_name, 0))


# ── Tab 1 — Overview ──────────────────────────────────────────────────────────
def tab_overview(students, df, course_names):
    avg_overall = round(df["score"].mean(), 1)
    top = df.loc[df["score"].idxmax()]
    low = df.loc[df["score"].idxmin()]

    course_avgs = {}
    for cn in course_names:
        vals = [student_mark(s, cn) for s in students]
        course_avgs[cn] = round(sum(vals) / len(vals), 1) if vals else 0

    display_courses = course_names[:3]
    kpi_items = [("Overall Weighted %", avg_overall, "#3b2007")] + [
        (cn + " Avg", course_avgs[cn], BROWN_PALETTE[i + 1])
        for i, cn in enumerate(display_courses)
    ]

    kpi_html = '<div style="display:grid;grid-template-columns:repeat(' + str(len(kpi_items)) + ',1fr);gap:1rem;margin-bottom:1.4rem">'
    for label, val, bg in kpi_items:
        kpi_html += (
            '<div style="background:' + bg + ';border-radius:12px;padding:1rem;text-align:center;'
            'box-shadow:2px 4px 12px ' + bg + '44">'
            '<div style="font-family:DM Mono,monospace;font-size:0.58rem;letter-spacing:0.15em;'
            'text-transform:uppercase;color:#c9a97888;margin-bottom:0.2rem">' + label + '</div>'
            '<div style="font-family:Playfair Display,serif;font-size:2rem;color:#f5ede0;line-height:1">'
            + str(val) + '</div></div>'
        )
    kpi_html += "</div>"
    st.markdown(kpi_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for col, student, label in [(col1, top, "🏆 Top Performer"), (col2, low, "📉 Needs Support")]:
        with col:
            g, rem, gcol = evaluate_grade(float(student["score"]))
            st.markdown(
                '<div style="background:#fdf6ec;border:1.5px solid #c9a978;'
                'border-top:4px solid ' + gcol + ';border-radius:12px;padding:1rem 1.2rem">'
                '<div style="font-family:DM Mono,monospace;font-size:0.6rem;text-transform:uppercase;'
                'letter-spacing:0.12em;color:#8b6340;margin-bottom:0.4rem">' + label + '</div>'
                '<div style="font-family:Playfair Display,serif;font-size:1.2rem;color:#3b2007;font-weight:700">'
                + str(student["name"]) + '</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.75rem;color:#6b3a1f;margin-top:4px">'
                'Roll ' + str(student["roll_no"]) + ' · ' + str(student["score"]) + '% · Grade '
                '<span style="color:' + gcol + ';font-weight:700">' + g + '</span></div>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("**Statistical Summary (Pandas)**")
    summary_data = {"Overall %": [s["score"] for s in students]}
    for cn in course_names:
        summary_data[cn] = [student_mark(s, cn) for s in students]
    st.dataframe(pd.DataFrame(summary_data).describe().round(2), use_container_width=True)


# ── Tab 2 — Grade Distribution ────────────────────────────────────────────────
def tab_grades(students):
    grades     = [evaluate_grade(s["score"])[0] for s in students]
    order      = ["A","B","C","D","F"]
    counts     = {g: grades.count(g) for g in order}
    labels     = [g for g in order if counts[g] > 0]
    values     = [counts[g] for g in labels]
    colors_map = {"A":"#557a3a","B":"#3a6b7a","C":"#7a6b3a","D":"#7a5030","F":"#8b2020"}
    bar_colors = [colors_map[g] for g in labels]
    n          = len(students)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(4.5, 3))
        style_fig(fig)
        bars = ax.bar(labels, values, color=bar_colors, width=0.5,
                      edgecolor="#fdf6ec", linewidth=1.5)
        ax.set_xlabel("Grade", color="#5a3e2b", fontsize=9)
        ax.set_ylabel("Students", color="#5a3e2b", fontsize=9)
        ax.set_title("Grade Distribution", color="#3b2007",
                     fontsize=10, fontfamily="serif", pad=8)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.05, str(val),
                    ha="center", color="#3b2007", fontsize=9, fontweight="bold")
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(4.5, 3))
        style_fig(fig2)
        ax2.pie(values, labels=labels, colors=bar_colors, autopct="%1.0f%%",
                pctdistance=0.75,
                wedgeprops=dict(width=0.55, edgecolor="#fdf6ec", linewidth=2),
                textprops={"color":"#3b2007","fontsize":9})
        ax2.set_title("Grade Share", color="#3b2007",
                      fontsize=10, fontfamily="serif", pad=8)
        plt.tight_layout(); st.pyplot(fig2); plt.close(fig2)

    st.markdown("**Breakdown**")
    for g in order:
        studs = [s for s in students if evaluate_grade(s["score"])[0] == g]
        if not studs: continue
        pct   = round(len(studs) / n * 100)
        col   = colors_map[g]
        names = ", ".join(s["name"] for s in studs)
        st.markdown(
            '<div style="display:flex;align-items:center;gap:1rem;padding:0.6rem 0.8rem;'
            'background:#fdf6ec;border-radius:8px;border-left:5px solid ' + col + ';margin-bottom:0.4rem">'
            '<div style="font-family:Playfair Display,serif;font-size:1.4rem;color:' + col + ';'
            'font-weight:700;min-width:28px">' + g + '</div>'
            '<div style="flex:1;background:#e8d0b0;border-radius:3px;height:10px;overflow:hidden">'
            '<div style="width:' + str(pct) + '%;background:' + col + ';height:100%;border-radius:3px"></div>'
            '</div>'
            '<div style="font-family:DM Mono,monospace;font-size:0.72rem;color:#6b3a1f;min-width:40px">'
            + str(pct) + '%</div>'
            '<div style="font-family:Lato,sans-serif;font-size:0.8rem;color:#5a3e2b">'
            + names + '</div></div>',
            unsafe_allow_html=True
        )


# ── Tab 3 — Subject Averages ──────────────────────────────────────────────────
def tab_subjects(students, course_names):
    if not course_names:
        no_data_card("No course data found. Register students with subject marks first.")
        return

    avgs = []
    for cn in course_names:
        vals = [student_mark(s, cn) for s in students]
        avgs.append(round(sum(vals) / len(vals), 1) if vals else 0)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, max(2.8, len(course_names) * 0.6)))
        style_fig(fig)
        pal  = [BROWN_PALETTE[i % len(BROWN_PALETTE)] for i in range(len(course_names))]
        bars = ax.barh(course_names, avgs, color=pal, height=0.5)
        ax.set_xlim(0, 110)
        ax.set_title("Average Score by Course", color="#3b2007",
                     fontsize=10, fontfamily="serif", pad=8)
        overall_avg = round(sum(avgs) / len(avgs), 1) if avgs else 0
        ax.axvline(x=overall_avg, color="#3b2007", linestyle="--",
                   linewidth=0.9, alpha=0.5, label="Class avg " + str(overall_avg) + "%")
        ax.legend(fontsize=7, facecolor="#fdf6ec", edgecolor="#c9a97855")
        for bar, val in zip(bars, avgs):
            ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                    str(val), va="center", color="#3b2007",
                    fontsize=8, fontweight="bold")
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    with col2:
        if len(course_names) >= 3:
            n_c      = len(course_names)
            angles   = np.linspace(0, 2 * np.pi, n_c, endpoint=False).tolist()
            vals_r   = avgs + avgs[:1]
            angles_r = angles + angles[:1]

            fig2, ax2 = plt.subplots(figsize=(4.5, 3.5), subplot_kw=dict(polar=True))
            style_fig(fig2, [ax2])
            ax2.plot(angles_r, vals_r, "o-", color="#8b4513", linewidth=2)
            ax2.fill(angles_r, vals_r, alpha=0.25, color="#c9a978")
            ax2.set_xticks(angles)
            short = [cn[:10] + "…" if len(cn) > 10 else cn for cn in course_names]
            ax2.set_xticklabels(short, color="#3b2007", fontsize=8)
            ax2.set_ylim(0, 100)
            ax2.set_yticks([25, 50, 75, 100])
            ax2.set_yticklabels(["25","50","75","100"], color="#8b6340", fontsize=7)
            ax2.grid(color="#c9a97844")
            ax2.set_title("Course Radar", color="#3b2007",
                          fontsize=10, fontfamily="serif", pad=14)
            plt.tight_layout(); st.pyplot(fig2); plt.close(fig2)
        else:
            fig2, ax2 = plt.subplots(figsize=(4.5, 3))
            style_fig(fig2)
            ax2.bar(course_names, avgs,
                    color=[BROWN_PALETTE[i] for i in range(len(course_names))],
                    width=0.4, edgecolor="#fdf6ec")
            ax2.set_ylim(0, 110)
            ax2.set_title("Course Averages", color="#3b2007",
                          fontsize=10, fontfamily="serif", pad=8)
            for i, val in enumerate(avgs):
                ax2.text(i, val + 1.5, str(val), ha="center",
                         color="#3b2007", fontsize=9, fontweight="bold")
            plt.tight_layout(); st.pyplot(fig2); plt.close(fig2)

    st.markdown("**Per-Student Marks (Pandas Table)**")
    table_data = {
        "Roll No.": [s["roll_no"] for s in students],
        "Name":     [s["name"]    for s in students],
    }
    for cn in course_names:
        table_data[cn] = [student_mark(s, cn) for s in students]
    table_data["Overall %"]   = [s["score"] for s in students]
    table_data["Best Course"] = [
        max(course_names, key=lambda cn: student_mark(s, cn))
        for s in students
    ]
    st.dataframe(pd.DataFrame(table_data).set_index("Roll No."), use_container_width=True)


# ── Tab 4 — Student Comparison ────────────────────────────────────────────────
def tab_comparison(students, course_names):
    if len(students) < 2:
        st.info("Add at least 2 students to compare.")
        return

    options = [s["roll_no"] + " — " + s["name"] for s in students]
    sel = st.multiselect(
        "Select students to compare (2 – 6)",
        options,
        default=options[:min(4, len(options))],
        key="cmp_sel"
    )
    if len(sel) < 2:
        st.warning("Select at least 2 students.")
        return

    chosen_rolls = [x.split(" — ")[0] for x in sel]
    chosen = [s for s in students if s["roll_no"] in chosen_rolls]
    names  = [s["name"] for s in chosen]
    pal    = [BROWN_PALETTE[i % len(BROWN_PALETTE)] for i in range(len(chosen))]

    if course_names:
        # ── Grouped bar ───────────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(max(6, len(chosen) * 2), 4))
        style_fig(fig)
        x     = np.arange(len(chosen))
        n_c   = len(course_names)
        width = min(0.6 / n_c, 0.18)

        for i, cn in enumerate(course_names):
            vals   = [student_mark(s, cn) for s in chosen]
            offset = (i - n_c / 2 + 0.5) * width
            label  = cn[:14] + "…" if len(cn) > 14 else cn
            ax.bar(x + offset, vals, width,
                   label=label,
                   color=BROWN_PALETTE[i % len(BROWN_PALETTE)],
                   edgecolor="#fdf6ec", linewidth=0.8)

        overall = [s["score"] for s in chosen]
        ax.plot(x, overall, "D--", color="#2c1a0e", linewidth=1.8,
                markersize=7, label="Overall %", zorder=5)

        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=15, ha="right",
                           fontsize=9, color="#3b2007")
        ax.set_ylim(0, 115)
        ax.set_title("Score Comparison by Course", color="#3b2007",
                     fontsize=10, fontfamily="serif")
        ax.legend(fontsize=7, facecolor="#fdf6ec", edgecolor="#c9a97855",
                  loc="upper right", ncol=min(4, n_c + 1))
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)

        # ── Line trend ────────────────────────────────────────────────────────
        if len(course_names) >= 2:
            fig2, ax2 = plt.subplots(
                figsize=(max(5, len(course_names) * 1.3), 3.5))
            style_fig(fig2)
            x_c = np.arange(len(course_names))

            for student, col, nm in zip(chosen, pal, names):
                vals = [student_mark(student, cn) for cn in course_names]
                ax2.plot(x_c, vals, "o-", color=col,
                         linewidth=2, markersize=7, label=nm)
                for xi, val in zip(x_c, vals):
                    ax2.annotate(str(val), (xi, val),
                                 textcoords="offset points", xytext=(0, 7),
                                 ha="center", fontsize=7, color=col)

            short = [cn[:10] + "…" if len(cn) > 10 else cn for cn in course_names]
            ax2.set_xticks(x_c)
            ax2.set_xticklabels(short, rotation=20, ha="right",
                                fontsize=8, color="#3b2007")
            ax2.set_ylim(0, 115)
            ax2.set_title("Course-wise Trend per Student", color="#3b2007",
                          fontsize=10, fontfamily="serif")
            ax2.legend(fontsize=7, facecolor="#fdf6ec", edgecolor="#c9a97855")
            plt.tight_layout(); st.pyplot(fig2); plt.close(fig2)

    # ── Ranking table ─────────────────────────────────────────────────────────
    st.markdown("**Ranking Table**")
    rank_data = []
    for s in chosen:
        row = {"Roll": s["roll_no"], "Name": s["name"],
               "Overall %": s["score"]}
        for cn in course_names:
            row[cn] = student_mark(s, cn)
        row["Grade"] = evaluate_grade(s["score"])[0]
        rank_data.append(row)

    rank_df = (pd.DataFrame(rank_data)
               .sort_values("Overall %", ascending=False)
               .reset_index(drop=True))
    rank_df.insert(0, "Rank", rank_df.index + 1)
    st.dataframe(rank_df.set_index("Rank"), use_container_width=True)


# ── Main render ───────────────────────────────────────────────────────────────
def render():
    st.subheader("📊  Analytics Dashboard")
    students = st.session_state.students

    if not students:
        no_data_card()
        return

    # Resolve course names ONCE here and pass to every tab
    course_names = get_course_names(students)

    # Show what courses are being used so user can verify
    if course_names:
        pills = "".join(
            '<span style="background:#e8d0b0;color:#6b3a1f;font-family:DM Mono,monospace;'
            'font-size:0.68rem;padding:2px 10px;border-radius:12px;margin-right:5px;'
            'border-left:3px solid #8b4513">' + cn + '</span>'
            for cn in course_names
        )
        st.markdown(
            '<div style="margin-bottom:1rem;font-family:DM Mono,monospace;'
            'font-size:0.7rem;color:#8b6340">Courses detected: ' + pills + '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("""<div class="warn-banner">
          ⚠ No course data found in student records.
          Go to <strong>Register Student → Course Setup</strong>, initialize your courses,
          then re-register your students.
        </div>""", unsafe_allow_html=True)
        return

    df = pd.DataFrame(students)
    t1, t2, t3, t4 = st.tabs([
        "🏠  Overview",
        "📊  Grade Distribution",
        "📐  Subject Averages",
        "⚖  Student Comparison",
    ])
    with t1: tab_overview(students, df, course_names)
    with t2: tab_grades(students)
    with t3: tab_subjects(students, course_names)
    with t4: tab_comparison(students, course_names)
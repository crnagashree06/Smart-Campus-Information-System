"""Home — Dashboard"""
import streamlit as st

PAGES = [
    ("📝", "Register Student",  "Enroll · Subjects · Grades",        "#8b4513"),
    ("🗂",  "Student Records",   "Display · Search · Sort · Fees",    "#6b3a1f"),
    ("📊", "Analytics",         "Charts · Grade dist · Comparisons", "#5c3317"),
    ("🔧", "System Tools",      "Directory scanner · File manager",  "#4a2810"),
]

# ── dot cluster helper (no f-string tricks) ───────────────────────────────────
_OPACITIES = ["55","33","55","22","44","33","55","33","22","55","44","22","33","55","33"]
_DOTS_HTML  = "".join(
    '<div style="width:5px;height:5px;border-radius:50%;background:#c9a978' + op + '"></div>'
    for op in _OPACITIES
)

def render():
    # ── Hero ──────────────────────────────────────────────────────────────────
    hero = (
        '<div style="position:relative;background:linear-gradient(120deg,#2c1a0e 0%,#5c3317 50%,#8b4513 100%);'
        'border-radius:20px;padding:2.5rem 2.5rem 2rem;margin-bottom:1.8rem;overflow:hidden;">'
        '<div style="position:absolute;top:-50px;right:-50px;width:200px;height:200px;'
        'border-radius:50%;border:2px solid #c9a97828;"></div>'
        '<div style="position:absolute;bottom:-25px;right:140px;width:80px;height:80px;'
        'transform:rotate(45deg);background:#ffffff07;border:1px solid #c9a97822;"></div>'
        '<div style="position:absolute;top:18px;right:60px;width:55px;height:55px;'
        'border-radius:50%;background:#c9a97820;"></div>'
        '<div style="position:absolute;inset:0;border-radius:20px;'
        'background:repeating-linear-gradient(-55deg,transparent,transparent 20px,'
        '#c9a97806 20px,#c9a97806 21px);pointer-events:none"></div>'
        '<div style="position:absolute;bottom:18px;right:24px;'
        'display:grid;grid-template-columns:repeat(5,7px);gap:5px">'
        + _DOTS_HTML +
        '</div>'
        '<p style="font-family:DM Mono,monospace;font-size:0.65rem;letter-spacing:0.22em;'
        'text-transform:uppercase;color:#c9a97888;margin-bottom:0.5rem">'
        'Dayananda Sagar College of Engineering · 1BPLC105B</p>'
        '<h1 style="font-family:Playfair Display,serif;font-size:clamp(1.8rem,4vw,2.9rem);'
        'line-height:1.1;color:#f5ede0;margin-bottom:0.45rem">'
        'Smart Campus <em style="color:#c9a978;font-style:italic">Information System</em></h1>'
        '<p style="color:#d4b89a;font-size:0.9rem;max-width:500px;line-height:1.7;margin:0">'
        'Register once. Every section reads from the same student registry automatically.'
        '</p></div>'
    )
    st.markdown(hero, unsafe_allow_html=True)

    # ── Live stats ────────────────────────────────────────────────────────────
    students = st.session_state.students
    courses  = st.session_state.courses
    n_s = len(students)
    n_c = len(courses)

    if n_s > 0:
        from modules.pg_register import evaluate_grade
        grade_counts = {}
        for s in students:
            g, _, _ = evaluate_grade(s["score"])
            grade_counts[g] = grade_counts.get(g, 0) + 1
        top = max(students, key=lambda s: s["score"])
        avg = round(sum(s["score"] for s in students) / n_s, 1)
    else:
        grade_counts, top, avg = {}, None, 0

    top_name  = top["name"]  if top else "—"
    top_score = top["score"] if top else ""

    stat_html = (
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.8rem">'
        + _stat_card("Students",    n_s,      "#3b2007", "circle")
        + _stat_card("Courses",     n_c,      "#5c3317",  "diamond")
        + _stat_card("Class Avg",   avg,      "#2c1a0e", "ring")
        + _stat_card_text("Top Student", top_name, top_score, "#3b2007")
        + '</div>'
    )
    st.markdown(stat_html, unsafe_allow_html=True)

    # ── Grade distribution snapshot ───────────────────────────────────────────
    if grade_counts:
        grade_order  = ["A", "B", "C", "D", "F"]
        grade_colors = {"A":"#557a3a","B":"#3a6b7a","C":"#7a6b3a","D":"#7a5030","F":"#8b2020"}
        bars_html = ""
        for g in grade_order:
            cnt  = grade_counts.get(g, 0)
            if cnt == 0:
                continue
            pct    = round(cnt / n_s * 100)
            col    = grade_colors[g]
            suffix = "s" if cnt != 1 else ""
            bars_html += (
                '<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.5rem">'
                '<div style="font-family:Playfair Display,serif;font-weight:700;font-size:1rem;'
                'color:' + col + ';min-width:18px">' + g + '</div>'
                '<div style="flex:1;background:#e8d0b0;border-radius:4px;height:12px;overflow:hidden">'
                '<div style="width:' + str(pct) + '%;background:' + col + ';height:100%;border-radius:4px"></div>'
                '</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.72rem;color:#6b3a1f;min-width:70px">'
                + str(cnt) + ' student' + suffix + '</div>'
                '</div>'
            )

        st.markdown(
            '<div style="background:#fdf6ec;border:1.5px solid #c9a978;border-radius:14px;'
            'padding:1.2rem 1.4rem;margin-bottom:1.8rem">'
            '<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:0.18em;'
            'text-transform:uppercase;color:#8b6340;margin-bottom:0.9rem">— Grade Distribution Snapshot</div>'
            + bars_html +
            '</div>',
            unsafe_allow_html=True
        )

    # ── Navigation tiles ──────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:0.18em;'
        'text-transform:uppercase;color:#8b6340;margin-bottom:0.9rem">— Sections</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)
    for i, (icon, title, desc, bar) in enumerate(PAGES):
        with cols[i]:
            st.markdown(
                '<div style="background:#fdf6ec;border:1.5px solid #e0c9a8;border-radius:14px;'
                'padding:1.2rem 1rem;border-top:5px solid ' + bar + ';'
                'box-shadow:2px 4px 12px #c9a97820;text-align:center">'
                '<div style="font-size:1.8rem;margin-bottom:0.5rem">' + icon + '</div>'
                '<div style="font-family:Playfair Display,serif;font-size:0.95rem;'
                'font-weight:700;color:#2c1a0e;margin-bottom:0.3rem">' + title + '</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.66rem;'
                'color:#8b6340;line-height:1.5">' + desc + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:2rem;background:#2c1a0e;border-radius:12px;padding:1rem 1.6rem;'
        'display:flex;align-items:center;justify-content:space-between;overflow:hidden;position:relative">'
        '<div style="position:absolute;inset:0;background:repeating-linear-gradient(90deg,'
        'transparent,transparent 22px,#c9a9780a 22px,#c9a9780a 23px);pointer-events:none"></div>'
        '<div style="font-family:Playfair Display,serif;font-size:0.9rem;color:#f5ede0;position:relative">'
        'Smart Campus Information System</div>'
        '<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#c9a97877;'
        'letter-spacing:0.12em;text-transform:uppercase;position:relative">'
        'Python Lab · 1BPLC105B / 205B</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ── Helper: numeric stat card ─────────────────────────────────────────────────
def _stat_card(label, value, bg, shape):
    deco = ""
    if shape == "circle":
        deco = '<div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;border-radius:50%;background:#c9a97814"></div>'
    elif shape == "diamond":
        deco = '<div style="position:absolute;bottom:-15px;left:-15px;width:60px;height:60px;transform:rotate(45deg);background:#c9a97814"></div>'
    elif shape == "ring":
        deco = '<div style="position:absolute;top:10px;right:10px;width:38px;height:38px;border-radius:50%;border:2px solid #c9a97838"></div>'
    return (
        '<div style="position:relative;background:' + bg + ';border-radius:16px;'
        'padding:1.4rem 1.2rem;overflow:hidden;border:1.5px solid #c9a97830;'
        'box-shadow:0 4px 20px ' + bg + '40">'
        + deco +
        '<div style="font-family:DM Mono,monospace;font-size:0.58rem;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#c9a97888;margin-bottom:0.3rem">' + label + '</div>'
        '<div style="font-family:Playfair Display,serif;font-size:2.6rem;color:#f5ede0;line-height:1">'
        + str(value) + '</div>'
        '<div style="margin-top:0.6rem;height:2px;background:linear-gradient(90deg,#c9a978,transparent);border-radius:2px"></div>'
        '</div>'
    )

def _stat_card_text(label, name, sub, bg):
    return (
        '<div style="position:relative;background:' + bg + ';border-radius:16px;'
        'padding:1.4rem 1.2rem;overflow:hidden;border:1.5px solid #c9a97830;'
        'box-shadow:0 4px 20px ' + bg + '40">'
        '<div style="position:absolute;bottom:-10px;right:-10px;width:50px;height:50px;'
        'transform:rotate(30deg);background:#c9a97818;border-radius:4px"></div>'
        '<div style="font-family:DM Mono,monospace;font-size:0.58rem;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#c9a97888;margin-bottom:0.3rem">' + label + '</div>'
        '<div style="font-family:Playfair Display,serif;font-size:1.1rem;color:#f5ede0;line-height:1.3;margin-top:0.2rem">'
        + str(name) + '</div>'
        '<div style="font-family:DM Mono,monospace;font-size:0.7rem;color:#c9a97888;margin-top:4px">'
        + str(sub) + '</div>'
        '<div style="margin-top:0.6rem;height:2px;background:linear-gradient(90deg,#c9a978,transparent);border-radius:2px"></div>'
        '</div>'
    )

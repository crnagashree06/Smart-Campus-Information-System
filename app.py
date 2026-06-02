"""
Smart Campus Information System — Restructured Navigation
"""
import streamlit as st

st.set_page_config(
    page_title="Smart Campus",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared state ─────────────────────────────────────────────────────────────
for key, default in [
    ("students",   []),
    ("courses",    []),
    ("m6_records", []),
    ("m7_tree",    {"folders": [], "files": {}}),
]:
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400;500&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; color: #2c1a0e; }

[data-testid="stAppViewContainer"] {
    background: #f5ede0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #2c1a0e 0%, #4a2810 55%, #6b3a1f 100%);
    border-right: 3px solid #c9a978;
}
[data-testid="stSidebar"] * { color: #f5ede0 !important; }
[data-testid="stSidebar"] hr { border-color: #c9a97844 !important; }

/* nav section labels */
.nav-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c9a97877;
    padding: 0.5rem 0 0.2rem;
    display: block;
}

.section-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: #e8d0b0;
    color: #6b3a1f;
    padding: 3px 10px;
    border-radius: 3px;
    margin-bottom: 6px;
    border-left: 3px solid #8b4513;
}

.output-card {
    background: linear-gradient(135deg, #fdf6ec 0%, #f5e6ce 100%);
    border: 1.5px solid #c9a978;
    border-left: 5px solid #8b4513;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.83rem;
    line-height: 1.9;
    color: #2c1a0e;
    min-height: 80px;
    box-shadow: 4px 4px 16px #c9a97828;
    position: relative;
    overflow: hidden;
}
.output-card::before {
    content:''; position:absolute; top:-30px; right:-30px;
    width:100px; height:100px; border-radius:50%; background:#c9a97812;
}
.output-placeholder { color:#b09070; font-style:italic; font-size:0.8rem; }

.result-row {
    display: flex; align-items: center; gap: 1rem;
    background: #fff8f0; border: 1px solid #e0c9a8;
    border-radius: 8px; padding: 0.65rem 1rem; margin-top: 0.45rem;
}
.result-label {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #8b6340; min-width: 95px;
}
.result-value {
    font-family: 'Playfair Display', serif; font-size: 1.05rem;
    color: #3b2007; font-weight: 700;
}
.info-banner {
    background: #e8d0b0; border-left: 4px solid #8b4513;
    border-radius: 8px; padding: 0.65rem 1rem;
    font-family: 'DM Mono', monospace; font-size: 0.74rem;
    color: #5a3020; margin-bottom: 1rem;
}
.warn-banner {
    background: #fce8d0; border-left: 4px solid #c0392b;
    border-radius: 8px; padding: 0.65rem 1rem;
    font-family: 'DM Mono', monospace; font-size: 0.74rem;
    color: #7a1a0e; margin-bottom: 1rem;
}
.stButton > button {
    background: linear-gradient(135deg, #6b3a1f, #8b4513) !important;
    color: #f5ede0 !important; border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    box-shadow: 2px 2px 8px #8b451328 !important;
    transition: all 0.18s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8b4513, #a0522d) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.74rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #8b6340 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #3b2007 !important;
    border-bottom: 2px solid #8b4513 !important;
}
input, select, textarea {
    background: #fdf6ec !important;
    border: 1.5px solid #c9a978 !important;
    border-radius: 8px !important;
    color: #2c1a0e !important;
}
hr { border-color: #c9a97855 !important; }
h2, h3 { font-family: 'Playfair Display', serif !important; color: #3b2007 !important; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#f5ede0; }
::-webkit-scrollbar-thumb { background:#c9a978; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 0.6rem'>
      <div style='font-family:Playfair Display,serif;font-size:1.6rem;color:#f5ede0'>
        🎓 Smart<span style='color:#c9a978'>Campus</span>
      </div>
      <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#c9a97877;
                  letter-spacing:0.15em;text-transform:uppercase;margin-top:5px'>
        Python Lab · 1BPLC105B
      </div>
    </div>
    """, unsafe_allow_html=True)

    n = len(st.session_state.students)
    st.markdown(f"""
    <div style='text-align:center;margin:0 0 0.8rem;font-family:DM Mono,monospace;font-size:0.7rem;
                color:{"#a8d898" if n>0 else "#e07070"}'>
      {"🟢" if n>0 else "🔴"} {n} student{"s" if n!=1 else ""} in registry
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("", [
        "🏠  Dashboard",
        "📝  Register Student",
        "🗂  Student Records",
        "📊  Analytics",
        "🔧  System Tools",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:0.62rem;
                color:#c9a97877;text-align:center;line-height:1.9'>
      Dayananda Sagar College<br>of Engineering<br>
      <span style='color:#c9a97844'>─────────────────</span><br>
      1BPLC105B / 205B
    </div>""", unsafe_allow_html=True)

# ── Route ─────────────────────────────────────────────────────────────────────
p = page.strip().split("  ")[-1]

if   p == "Dashboard":        from modules.pg_home      import render
elif p == "Register Student": from modules.pg_register  import render
elif p == "Student Records":  from modules.pg_records   import render
elif p == "Analytics":        from modules.pg_analytics import render
elif p == "System Tools":     from modules.pg_tools     import render
else:                         from modules.pg_home      import render

render()

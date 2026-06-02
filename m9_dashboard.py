"""Module 09 — Smart Campus Dashboard (geometric · flashy · brown & beige)"""
import streamlit as st

MODULES = [
    {"num":"01","icon":"📝","name":"Grade Evaluation",      "sub":"if · elif · else"},
    {"num":"02","icon":"📚","name":"Enrollment Mgmt",       "sub":"while · for · break"},
    {"num":"03","icon":"🗂️","name":"Student Records",       "sub":"list · dict · set"},
    {"num":"04","icon":"🔍","name":"Sort & Search",         "sub":"bubble · binary"},
    {"num":"05","icon":"💰","name":"Fee Calculation",       "sub":"functions · defaults"},
    {"num":"06","icon":"🗒️","name":"File Handling",         "sub":"read · write · process"},
    {"num":"07","icon":"📂","name":"Directory Scan",        "sub":"os · exceptions"},
    {"num":"08","icon":"📊","name":"Performance Analytics", "sub":"numpy · pandas · matplotlib"},
]

def render():
    st.markdown('<span class="section-tag">mini project · integration</span>', unsafe_allow_html=True)
    st.subheader("09 · Smart Campus — System Dashboard")

    # ── Hero banner with geometry ──────────────────────────────────────────
    st.markdown("""
    <div style="position:relative;background:linear-gradient(135deg,#2c1a0e 0%,#5c3317 45%,#8b4513 100%);
                border-radius:20px;padding:2.5rem 2rem;margin-bottom:2rem;overflow:hidden;
                box-shadow:0 8px 40px #3b200740">

      <!-- big circle top-right -->
      <div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;
                  border-radius:50%;border:2px solid #c9a97830;"></div>
      <!-- smaller filled circle -->
      <div style="position:absolute;top:20px;right:40px;width:80px;height:80px;
                  border-radius:50%;background:#c9a97818;"></div>
      <!-- rotated square (diamond) -->
      <div style="position:absolute;bottom:-25px;right:160px;width:70px;height:70px;
                  transform:rotate(45deg);background:#ffffff08;border:1px solid #c9a97825;"></div>
      <!-- thin diagonal stripe accent -->
      <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                  background:repeating-linear-gradient(
                    -55deg,transparent,transparent 18px,
                    #c9a97808 18px,#c9a97808 19px);
                  border-radius:20px;pointer-events:none;"></div>

      <!-- small dot cluster -->
      <div style="position:absolute;bottom:20px;right:30px;
                  display:grid;grid-template-columns:repeat(4,8px);gap:6px">
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97855"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97835"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97855"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97835"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97835"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97855"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97835"></div>
        <div style="width:6px;height:6px;border-radius:50%;background:#c9a97855"></div>
      </div>

      <div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:0.22em;
                  text-transform:uppercase;color:#c9a97899;margin-bottom:0.5rem">
        System Overview · All Modules Active
      </div>
      <div style="font-family:Playfair Display,serif;font-size:2.2rem;
                  line-height:1.1;color:#f5ede0;margin-bottom:0.4rem">
        Smart Campus
        <em style="color:#c9a978;font-style:italic">Dashboard</em>
      </div>
      <div style="color:#d4b896;font-size:0.88rem;max-width:440px;line-height:1.65">
        8 integrated Python modules. Use the sidebar to navigate to any lab.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live stats ──────────────────────────────────────────────────────────
    m3_n = len(st.session_state.get("m3_students", []))
    m8_n = len(st.session_state.get("m8_students", []))
    m2_n = len(st.session_state.get("m2_courses",  []))
    m6_n = len(st.session_state.get("m6_records",  []))

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem">

      <!-- stat 1 -->
      <div style="position:relative;background:#3b2007;border-radius:16px;padding:1.4rem 1.2rem;
                  overflow:hidden;box-shadow:0 4px 20px #3b200740">
        <div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;
                    border-radius:50%;background:#c9a97815"></div>
        <div style="font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:0.16em;
                    text-transform:uppercase;color:#c9a97899;margin-bottom:0.4rem">Students Registered</div>
        <div style="font-family:Playfair Display,serif;font-size:2.8rem;color:#f5ede0;
                    line-height:1">{m3_n + m8_n}</div>
        <div style="margin-top:0.7rem;height:3px;background:linear-gradient(90deg,#c9a978,transparent);border-radius:2px"></div>
      </div>

      <!-- stat 2 -->
      <div style="position:relative;background:linear-gradient(135deg,#5c3317,#7a4a25);
                  border-radius:16px;padding:1.4rem 1.2rem;overflow:hidden;
                  box-shadow:0 4px 20px #3b200740">
        <div style="position:absolute;bottom:-15px;left:-15px;width:60px;height:60px;
                    transform:rotate(45deg);background:#c9a97815"></div>
        <div style="font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:0.16em;
                    text-transform:uppercase;color:#f5ede077;margin-bottom:0.4rem">Courses Enrolled</div>
        <div style="font-family:Playfair Display,serif;font-size:2.8rem;color:#f5ede0;line-height:1">{m2_n}</div>
        <div style="margin-top:0.7rem;height:3px;background:linear-gradient(90deg,#f5ede055,transparent);border-radius:2px"></div>
      </div>

      <!-- stat 3 -->
      <div style="position:relative;background:#2c1a0e;border-radius:16px;padding:1.4rem 1.2rem;
                  overflow:hidden;border:1.5px solid #c9a97840;
                  box-shadow:0 4px 20px #3b200740">
        <div style="position:absolute;top:10px;right:10px;width:40px;height:40px;
                    border-radius:50%;border:2px solid #c9a97840"></div>
        <div style="font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:0.16em;
                    text-transform:uppercase;color:#c9a97899;margin-bottom:0.4rem">File Records</div>
        <div style="font-family:Playfair Display,serif;font-size:2.8rem;color:#c9a978;line-height:1">{m6_n}</div>
        <div style="margin-top:0.7rem;height:3px;background:linear-gradient(90deg,#c9a978aa,transparent);border-radius:2px"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Module tiles ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:DM Mono,monospace;font-size:0.65rem;letter-spacing:0.18em;
                text-transform:uppercase;color:#8b6340;margin-bottom:1rem">
    — All Modules
    </div>
    """, unsafe_allow_html=True)

    tiles_html = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:0.9rem;margin-bottom:2rem">'
    for i, m in enumerate(MODULES):
        # alternate accent bar colour
        bar = "#8b4513" if i % 2 == 0 else "#c9a978"
        tiles_html += f"""
        <div style="background:#fdf6ec;border:1.5px solid #e0c9a8;border-radius:14px;
                    padding:1rem 1.1rem;display:flex;align-items:center;gap:0.9rem;
                    border-left:5px solid {bar};
                    box-shadow:2px 2px 10px #c9a97820;
                    transition:transform 0.2s">
          <div style="font-size:1.4rem;min-width:2rem;text-align:center">{m['icon']}</div>
          <div style="flex:1">
            <div style="font-family:Playfair Display,serif;font-size:0.92rem;
                        font-weight:700;color:#2c1a0e">Lab {m['num']} · {m['name']}</div>
            <div style="font-family:DM Mono,monospace;font-size:0.67rem;
                        color:#8b6340;margin-top:3px">{m['sub']}</div>
          </div>
          <div style="font-family:DM Mono,monospace;font-size:0.6rem;padding:3px 8px;
                      border-radius:4px;background:#e8d0b0;color:#6b3a1f;
                      border-left:2px solid {bar}">READY</div>
        </div>"""
    tiles_html += "</div>"
    st.markdown(tiles_html, unsafe_allow_html=True)

    # ── Decorative footer strip ─────────────────────────────────────────────
    st.markdown("""
    <div style="position:relative;background:#2c1a0e;border-radius:14px;padding:1.2rem 1.8rem;
                overflow:hidden;display:flex;align-items:center;justify-content:space-between">

      <!-- repeating diamond pattern -->
      <div style="position:absolute;inset:0;
                  background:repeating-linear-gradient(
                    90deg,transparent,transparent 24px,
                    #c9a97810 24px,#c9a97810 25px);
                  pointer-events:none"></div>

      <div style="font-family:Playfair Display,serif;font-size:0.9rem;color:#f5ede0;position:relative">
        Smart Campus Information System
      </div>
      <div style="font-family:DM Mono,monospace;font-size:0.62rem;
                  color:#c9a97888;letter-spacing:0.12em;text-transform:uppercase;position:relative">
        Python Lab · 1BPLC105B / 205B
      </div>
    </div>
    """, unsafe_allow_html=True)

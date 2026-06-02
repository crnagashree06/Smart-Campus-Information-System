"""Module 08 — Student Performance Analytics (numpy · pandas · matplotlib)"""
import streamlit as st
import numpy as np, pandas as pd, matplotlib, matplotlib.pyplot as plt
matplotlib.use("Agg")

def render():
    st.markdown('<span class="section-tag">numpy · pandas · matplotlib</span>', unsafe_allow_html=True)
    st.subheader("08 · Student Performance Analytics")

    if "m8_students" not in st.session_state:
        st.session_state.m8_students = []

    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.markdown("**Add Student Scores**")
        c1,c2,c3,c4,c5 = st.columns([2,1,1,1,1])
        with c1: sn = st.text_input("Name", placeholder="Name", key="m8_name", label_visibility="collapsed")
        with c2: ma = st.number_input("Math", 0, 100, step=1, key="m8_math", label_visibility="collapsed")
        with c3: sc = st.number_input("Sci",  0, 100, step=1, key="m8_sci",  label_visibility="collapsed")
        with c4: en = st.number_input("Eng",  0, 100, step=1, key="m8_eng",  label_visibility="collapsed")
        with c5:
            if st.button("+ Add", key="m8_add"):
                if sn.strip():
                    st.session_state.m8_students.append({"name":sn.strip(),"math":int(ma),"sci":int(sc),"eng":int(en)}); st.rerun()

        for i, s in enumerate(st.session_state.m8_students):
            r1, r2 = st.columns([5,1])
            with r1: st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:0.78rem;padding:3px 0;color:#3b2007'>{s['name']} — M:{s['math']} S:{s['sci']} E:{s['eng']}</div>", unsafe_allow_html=True)
            with r2:
                if st.button("✕", key=f"m8_del_{i}"):
                    st.session_state.m8_students.pop(i); st.rerun()
        if not st.session_state.m8_students: st.caption("No data yet.")

        b1,b2 = st.columns(2)
        with b1: run = st.button("▶  Analyze", key="m8_run", type="primary")
        with b2:
            if st.button("Clear", key="m8_clear"):
                st.session_state.m8_students=[]; st.rerun()

    with col_out:
        st.markdown("**Result**")
        if run:
            students = st.session_state.m8_students
            if len(students) < 2:
                st.error("Add at least 2 students.")
            else:
                df = pd.DataFrame(students)
                def stats(col):
                    a = np.array(df[col], dtype=float)
                    return round(float(np.mean(a)),1), round(float(np.median(a)),1), round(float(np.std(a)),2)

                avgM,medM,stdM = stats("math")
                avgS,medS,stdS = stats("sci")
                avgE,medE,stdE = stats("eng")
                top_m = df.loc[df["math"].idxmax(),"name"]
                top_s = df.loc[df["sci"].idxmax(), "name"]
                top_e = df.loc[df["eng"].idxmax(), "name"]

                st.markdown(f"""
                <div class="output-card">
                  <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#8b6340;margin-bottom:0.8rem">Statistical Summary</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.5rem;margin-bottom:0.8rem">
                    <div style="background:#3b2007;border-radius:8px;padding:0.6rem;text-align:center">
                      <div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#c9a978;text-transform:uppercase">Math</div>
                      <div style="font-family:Playfair Display,serif;font-size:1.3rem;color:#f5ede0">{avgM}</div>
                      <div style="font-size:0.65rem;color:#c9a97888">avg</div>
                    </div>
                    <div style="background:#3b2007;border-radius:8px;padding:0.6rem;text-align:center">
                      <div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#c9a978;text-transform:uppercase">Science</div>
                      <div style="font-family:Playfair Display,serif;font-size:1.3rem;color:#f5ede0">{avgS}</div>
                      <div style="font-size:0.65rem;color:#c9a97888">avg</div>
                    </div>
                    <div style="background:#3b2007;border-radius:8px;padding:0.6rem;text-align:center">
                      <div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#c9a978;text-transform:uppercase">English</div>
                      <div style="font-family:Playfair Display,serif;font-size:1.3rem;color:#f5ede0">{avgE}</div>
                      <div style="font-size:0.65rem;color:#c9a97888">avg</div>
                    </div>
                  </div>
                  <div class="result-row"><span class="result-label">Top Math</span><span class="result-value">{top_m}</span></div>
                  <div class="result-row"><span class="result-label">Top Sci</span><span class="result-value">{top_s}</span></div>
                  <div class="result-row"><span class="result-label">Top Eng</span><span class="result-value">{top_e}</span></div>
                </div>
                """, unsafe_allow_html=True)

                # Chart
                fig, ax = plt.subplots(figsize=(5, 2.2))
                fig.patch.set_facecolor("#fdf6ec")
                ax.set_facecolor("#fdf6ec")
                subjects = ["Math","Science","English"]
                avgs     = [avgM, avgS, avgE]
                colors   = ["#6b3a1f","#8b4513","#c9a978"]
                bars = ax.barh(subjects, avgs, color=colors, height=0.45)
                ax.set_xlim(0,100)
                ax.tick_params(colors="#5a3e2b", labelsize=8)
                for spine in ax.spines.values(): spine.set_edgecolor("#c9a97866")
                for bar, val in zip(bars, avgs):
                    ax.text(val+1, bar.get_y()+bar.get_height()/2, str(val), va="center", color="#3b2007", fontsize=8)
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)
        else:
            st.markdown('<div class="output-card"><span class="output-placeholder">↖ Add student data and click Analyze</span></div>', unsafe_allow_html=True)

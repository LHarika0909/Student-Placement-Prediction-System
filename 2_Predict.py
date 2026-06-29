import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os, glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_feature_columns
from utils.model import train_models, load_best_model, predict_placement

st.set_page_config(page_title="Predict · PlacementIQ", page_icon="🔮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{ font-family:'Inter',sans-serif; }
.stApp{ background-color:#0F0F1A; }
[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0D0D1F,#1A1A2E); border-right:1px solid rgba(108,99,255,0.2); }
.section-header{ font-family:'Space Grotesk',sans-serif; font-size:1.4rem; font-weight:700; color:#E8E8F0; margin:28px 0 18px; padding-bottom:10px; border-bottom:2px solid rgba(108,99,255,0.4); }
.stButton>button{ background:linear-gradient(135deg,#6C63FF,#8B5CF6)!important; color:white!important; border:none!important; border-radius:10px!important; font-weight:600!important; font-size:1rem!important; padding:14px 40px!important; width:100%!important; }
hr{ border-color:rgba(108,99,255,0.2)!important; }
::-webkit-scrollbar{ width:6px; } ::-webkit-scrollbar-thumb{ background:#6C63FF; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A1A2E,#16213E);border:1px solid rgba(108,99,255,0.25);
            border-radius:20px;padding:36px 40px;margin-bottom:28px;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:800;color:#E8E8F0;">
        🔮 Placement Predictor
    </div>
    <div style="font-size:0.95rem;color:#9090A8;margin-top:8px;">
        Enter student profile below to receive an AI-powered placement prediction.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Train model ───────────────────────────────────────────────
df           = load_data()
feature_cols = get_feature_columns()

if "model_trained" not in st.session_state:
    model_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models"
    )
    for f in glob.glob(os.path.join(model_dir, "*.pkl")):
        os.remove(f)
    with st.spinner("⚡ Training models on latest data..."):
        results, best_name, _, _ = train_models(df, feature_cols)
        st.session_state["model_trained"]    = True
        st.session_state["best_model_name"]  = best_name

model, scaler, features, needs_scale = load_best_model()

if model is None:
    with st.spinner("⚡ Training models..."):
        results, best_name, _, _ = train_models(df, feature_cols)
        st.session_state["model_trained"]   = True
        st.session_state["best_model_name"] = best_name
    model, scaler, features, needs_scale = load_best_model()

st.markdown(f"""
<div style="background:rgba(108,99,255,0.1);border:1px solid rgba(108,99,255,0.3);
            border-radius:10px;padding:12px 18px;margin-bottom:24px;font-size:0.85rem;color:#A09CF7;">
    ✦ Active Model: <strong>{st.session_state.get('best_model_name','Best Model')}</strong>
    — selected automatically based on highest accuracy.
</div>
""", unsafe_allow_html=True)

# ── Sliders ───────────────────────────────────────────────────
st.markdown('<div class="section-header">Academic Profile</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    cgpa         = st.slider("CGPA", 0.0, 10.0, 7.5, 0.1)
    internships  = st.slider("Internships", 0, 5, 1)
    projects     = st.slider("Projects", 0, 10, 2)
with c2:
    workshops    = st.slider("Workshops / Seminars", 0, 10, 2)
    backlogs     = st.slider("Backlogs", 0, 10, 0)
    comm         = st.slider("Communication Skill (1–10)", 1, 10, 7)
with c3:
    aptitude     = st.slider("Aptitude Score (0–100)", 0, 100, 70)
    technical    = st.slider("Technical Score (0–100)", 0, 100, 72)
    soft_skill   = st.slider("Soft Skill Score (0–100)", 0, 100, 68)

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Placement Chances", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────
if predict_btn:
    input_data = {
        "cgpa": cgpa, "internships": internships, "projects": projects,
        "workshops": workshops, "backlogs": backlogs,
        "communication_skill": comm, "aptitude_score": aptitude,
        "technical_score": technical, "soft_skill_score": soft_skill,
    }

    prediction, probability = predict_placement(model, scaler, features, needs_scale, input_data)

    st.markdown('<div class="section-header">Prediction Result</div>', unsafe_allow_html=True)

    if prediction == 1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(52,211,153,0.1),rgba(16,185,129,0.05));
                    border:2px solid rgba(52,211,153,0.4);border-radius:20px;
                    padding:40px;text-align:center;margin:20px 0;">
            <div style="font-size:3.5rem;margin-bottom:12px;">🎉</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;
                        font-weight:800;color:#34D399;">LIKELY TO BE PLACED</div>
            <div style="font-size:3rem;font-weight:800;color:#E8E8F0;margin:14px 0;">{probability}%</div>
            <div style="font-size:0.9rem;color:#9090A8;">Placement Probability Score</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(239,68,68,0.1),rgba(220,38,38,0.05));
                    border:2px solid rgba(239,68,68,0.4);border-radius:20px;
                    padding:40px;text-align:center;margin:20px 0;">
            <div style="font-size:3.5rem;margin-bottom:12px;">⚠️</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;
                        font-weight:800;color:#EF4444;">NEEDS IMPROVEMENT</div>
            <div style="font-size:3rem;font-weight:800;color:#E8E8F0;margin:14px 0;">{probability}%</div>
            <div style="font-size:0.9rem;color:#9090A8;">Placement Probability Score</div>
        </div>""", unsafe_allow_html=True)

    # Profile chart
    st.markdown('<div class="section-header">Profile Breakdown</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=list(input_data.keys()), y=list(input_data.values()),
        marker=dict(color=list(input_data.values()),
                    colorscale=[[0,"#EF4444"],[0.5,"#F59E0B"],[1,"#6C63FF"]],
                    line_width=0)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E8E8F0"),
        title="Your Input Profile Values",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(t=40,b=40,l=20,r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tips
    if prediction == 0:
        st.markdown('<div class="section-header">💡 Improvement Recommendations</div>',
                    unsafe_allow_html=True)
        tips = []
        if cgpa       < 7.0: tips.append(("📚","Improve CGPA","Aim for 7.5+ CGPA. Focus on weak subjects."))
        if internships == 0:  tips.append(("💼","Get Internship","Apply on LinkedIn, Internshala, or college portal."))
        if projects    < 2:   tips.append(("🛠️","Build Projects","Work on 2–3 personal or open-source projects."))
        if aptitude   < 60:   tips.append(("🧠","Boost Aptitude","Practice with IndiaBix or PrepInsta daily."))
        if comm        < 6:   tips.append(("🗣️","Communication","Join public speaking clubs or workshops."))
        if not tips:          tips.append(("✨","You're Close!","Fine-tune weaker areas and apply to more companies."))

        tip_cols = st.columns(len(tips))
        for tc, (icon, title, desc) in zip(tip_cols, tips):
            tc.markdown(f"""
            <div style="background:#1A1A2E;border:1px solid rgba(108,99,255,0.25);
                        border-radius:14px;padding:20px;margin-bottom:12px;">
                <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
                <div style="font-weight:700;color:#E8E8F0;font-size:0.88rem;margin-bottom:8px;">{title}</div>
                <div style="font-size:0.78rem;color:#9090A8;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)
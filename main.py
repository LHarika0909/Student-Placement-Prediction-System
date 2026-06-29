import streamlit as st

st.set_page_config(
    page_title="PlacementIQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D1F 0%, #1A1A2E 100%);
    border-right: 1px solid rgba(108,99,255,0.2);
}
[data-testid="stSidebar"] * { color: #E8E8F0 !important; }

/* Main background */
.stApp { background-color: #0F0F1A; }

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(108,99,255,0.7);
}
.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #6C63FF;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #9090A8;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 6px;
}

/* Section headers */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #E8E8F0;
    margin: 32px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(108,99,255,0.4);
}

/* Badges */
.badge-placed {
    background: rgba(52,211,153,0.15);
    color: #34D399;
    border: 1px solid rgba(52,211,153,0.4);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-not-placed {
    background: rgba(239,68,68,0.15);
    color: #EF4444;
    border: 1px solid rgba(239,68,68,0.4);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Hero */
.hero-container {
    background: linear-gradient(135deg, #1A1A2E 0%, #0D0D1F 50%, #16213E 100%);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 24px;
    padding: 52px 48px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #E8E8F0;
    line-height: 1.1;
    margin: 0;
}
.hero-title span { color: #6C63FF; }
.hero-sub {
    font-size: 1.05rem;
    color: #9090A8;
    margin-top: 14px;
    max-width: 520px;
    line-height: 1.65;
}
.hero-pill {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.4);
    color: #A09CF7;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    margin-bottom: 18px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 28px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(108,99,255,0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1A1A2E;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #9090A8 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#6C63FF,#8B5CF6) !important;
    color: white !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] { accent-color: #6C63FF; }

/* Inputs */
.stNumberInput input, .stSelectbox select {
    background: #1A1A2E !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    color: #E8E8F0 !important;
    border-radius: 8px !important;
}

/* Divider */
hr { border-color: rgba(108,99,255,0.2) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F0F1A; }
::-webkit-scrollbar-thumb { background: #6C63FF; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-family: Space Grotesk, sans-serif; font-size: 1.5rem; font-weight: 800; color: #E8E8F0;'>
            🎓 PlacementIQ
        </div>
        <div style='font-size: 0.75rem; color: #6C63FF; font-weight: 500; margin-top: 4px;'>
            AI-POWERED PREDICTION SYSTEM
        </div>
    </div>
    <hr style='border-color: rgba(108,99,255,0.3); margin-bottom: 20px;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size: 0.72rem; color: #9090A8; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 10px;'>
        Navigation
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠  Home", )
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard")
    st.page_link("pages/2_Predict.py", label="🔮  Predict Placement")
    st.page_link("pages/3_Analytics.py", label="📈  Analytics & Models")

    st.markdown("""
    <hr style='border-color: rgba(108,99,255,0.2); margin: 24px 0 16px 0;'>
    <div style='font-size: 0.72rem; color: #9090A8; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 10px;'>
        About
    </div>
    <div style='font-size: 0.8rem; color: #9090A8; line-height: 1.6;'>
        Predicts student placement outcomes using machine learning models trained on academic & skill data.
    </div>
    <div style='margin-top: 20px; font-size: 0.72rem; color: rgba(108,99,255,0.6);'>
        v1.0.0 · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# ── Home Page ─────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-pill">✦ Machine Learning · Classification · Analytics</div>
    <h1 class="hero-title">Student <span>Placement</span><br>Prediction System</h1>
    <p class="hero-sub">
        Harness the power of multiple ML classifiers to predict campus placement outcomes.
        Analyze academic performance, skills, and experiences — all in one platform.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
cards = [
    ("4", "ML Models Trained", "#6C63FF"),
    ("9", "Feature Variables", "#8B5CF6"),
    ("95%+", "Model Accuracy", "#34D399"),
    ("Real-time", "Predictions", "#F59E0B"),
]
for col, (val, label, color) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color};">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="section-header">How It Works</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
steps = [
    ("📥", "1. Data Collection", "Academic records including CGPA, internships, projects, skills, and more are compiled into a structured dataset."),
    ("🤖", "2. Model Training", "Four classifiers — Random Forest, Gradient Boosting, Logistic Regression, and SVM — are trained and compared."),
    ("🔮", "3. Prediction", "Enter a student's profile and receive instant placement predictions with probability scores."),
]
for col, (icon, title, desc) in zip([c1, c2, c3], steps):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:left; padding: 28px;">
            <div style="font-size: 2rem; margin-bottom: 14px;">{icon}</div>
            <div style="font-family: Space Grotesk, sans-serif; font-weight: 700; font-size: 1rem; color: #E8E8F0; margin-bottom: 10px;">{title}</div>
            <div style="font-size: 0.82rem; color: #9090A8; line-height: 1.65;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="section-header">Features Used for Prediction</div>
""", unsafe_allow_html=True)

features = [
    ("📚", "CGPA", "Cumulative Grade Point Average"),
    ("💼", "Internships", "Number of internships completed"),
    ("🛠️", "Projects", "Academic & personal projects"),
    ("🎓", "Workshops", "Seminars and workshops attended"),
    ("⚠️", "Backlogs", "Number of pending backlogs"),
    ("🗣️", "Communication", "Communication skill rating (1–10)"),
    ("🧠", "Aptitude Score", "Quantitative aptitude test score"),
    ("💻", "Technical Score", "Technical proficiency score"),
    ("🤝", "Soft Skills", "Soft skill assessment score"),
]

cols = st.columns(3)
for i, (icon, name, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background: #1A1A2E; border: 1px solid rgba(108,99,255,0.2); border-radius: 10px;
                    padding: 14px 16px; margin-bottom: 12px; display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.2rem;">{icon}</span>
            <div>
                <div style="font-weight: 600; color: #E8E8F0; font-size: 0.85rem;">{name}</div>
                <div style="font-size: 0.75rem; color: #9090A8; margin-top: 2px;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
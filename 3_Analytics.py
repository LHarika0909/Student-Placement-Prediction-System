import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_feature_columns
from utils.model import train_models

st.set_page_config(page_title="Analytics - PlacementIQ", page_icon="📈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{ font-family:'Inter',sans-serif; }
.stApp{ background-color:#0F0F1A; }
[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0D0D1F,#1A1A2E); border-right:1px solid rgba(108,99,255,0.2); }
.section-header{ font-family:'Space Grotesk',sans-serif; font-size:1.4rem; font-weight:700; color:#E8E8F0; margin:28px 0 18px; padding-bottom:10px; border-bottom:2px solid rgba(108,99,255,0.4); }
hr{ border-color:rgba(108,99,255,0.2)!important; }
::-webkit-scrollbar{ width:6px; }
::-webkit-scrollbar-thumb{ background:#6C63FF; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E8E8F0"),
    margin=dict(t=50, b=40, l=20, r=20)
)

MC = {
    "Random Forest":       "#6C63FF",
    "Gradient Boosting":   "#60A5FA",
    "Logistic Regression": "#34D399",
    "SVM":                 "#F59E0B",
}

st.markdown("""
<div style="background:linear-gradient(135deg,#1A1A2E,#16213E);border:1px solid rgba(108,99,255,0.25);border-radius:20px;padding:36px 40px;margin-bottom:28px;">
<div style="font-family:Space Grotesk,sans-serif;font-size:2rem;font-weight:800;color:#E8E8F0;">Model Analytics</div>
<div style="font-size:0.95rem;color:#9090A8;margin-top:8px;">Compare all trained classifiers, view confusion matrices, and analyze feature importance.</div>
</div>
""", unsafe_allow_html=True)

df = load_data()
feature_cols = get_feature_columns()

if "analytics_results" not in st.session_state:
    with st.spinner("Training all models..."):
        results, best_name, _, _ = train_models(df, feature_cols)
        st.session_state["analytics_results"] = results
        st.session_state["analytics_best"] = best_name

results   = st.session_state["analytics_results"]
best_name = st.session_state["analytics_best"]
names     = list(results.keys())

# ── Model Cards ───────────────────────────────────────────────
st.markdown('<div class="section-header">Model Comparison</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
cols_list = [c1, c2, c3, c4]

for i, name in enumerate(names):
    res   = results[name]
    color = MC.get(name, "#6C63FF")
    is_best = (name == best_name)

    if is_best:
        border = "2px solid #6C63FF"
        badge  = '<div style="background:rgba(108,99,255,0.2);color:#A09CF7;font-size:0.6rem;font-weight:700;padding:2px 8px;border-radius:8px;display:inline-block;margin-bottom:8px;">BEST MODEL</div>'
    else:
        border = "1px solid rgba(108,99,255,0.25)"
        badge  = '<div style="height:22px;"></div>'

    acc     = str(res["accuracy"]) + "%"
    auc_val = str(res["auc"])
    cv_val  = str(res["cv_mean"]) + "%"

    card = (
        '<div style="background:linear-gradient(135deg,#1A1A2E,#16213E);'
        'border:' + border + ';border-radius:16px;padding:22px 18px;text-align:center;margin-bottom:8px;">'
        + badge +
        '<div style="font-size:0.68rem;color:#9090A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">' + name + '</div>'
        '<div style="font-size:2.2rem;font-weight:800;color:' + color + ';font-family:Space Grotesk,sans-serif;">' + acc + '</div>'
        '<div style="font-size:0.72rem;color:#9090A8;margin-bottom:12px;">Accuracy</div>'
        '<div style="display:flex;justify-content:space-around;font-size:0.76rem;color:#9090A8;'
        'border-top:1px solid rgba(108,99,255,0.15);padding-top:10px;margin-top:4px;">'
        '<span>AUC <b style="color:#E8E8F0;">' + auc_val + '</b></span>'
        '<span>CV <b style="color:#E8E8F0;">' + cv_val + '</b></span>'
        '</div></div>'
    )

    cols_list[i].markdown(card, unsafe_allow_html=True)

# ── Accuracy Bar + Radar ───────────────────────────────────────
st.markdown('<div class="section-header">Accuracy Comparison</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)
accs = [results[n]["accuracy"] for n in names]
clrs = [MC[n] for n in names]

with ch1:
    fig = go.Figure(go.Bar(x=names, y=accs, marker_color=clrs, marker_line_width=0))
    fig.update_layout(**PL, title="Model Accuracy (%)", title_font_size=15,
                      yaxis=dict(range=[0,110], gridcolor="rgba(255,255,255,0.05)"),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
    st.plotly_chart(fig, use_container_width=True)

with ch2:
    fig2 = go.Figure(go.Scatterpolar(
        r=accs + [accs[0]], theta=names + [names[0]], fill="toself",
        fillcolor="rgba(108,99,255,0.15)", line=dict(color="#6C63FF", width=2)
    ))
    fig2.update_layout(
        **PL, title="Radar - Accuracy", title_font_size=15,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,110], gridcolor="rgba(255,255,255,0.08)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.08)")
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Confusion Matrices ─────────────────────────────────────────
st.markdown('<div class="section-header">Confusion Matrices</div>', unsafe_allow_html=True)
cm1, cm2, cm3, cm4 = st.columns(4)
cm_cols = [cm1, cm2, cm3, cm4]

for i, name in enumerate(names):
    cm = results[name]["confusion_matrix"]
    fig = go.Figure(go.Heatmap(
        z=cm,
        x=["Not Placed", "Placed"],
        y=["Not Placed", "Placed"],
        colorscale=[[0, "#1A1A2E"], [1, MC[name]]],
        text=[[str(v) for v in row] for row in cm],
        texttemplate="<b>%{text}</b>",
        showscale=False,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E8E8F0"),
        title=name, title_font_size=11,
        margin=dict(t=40, b=30, l=20, r=20)
    )
    cm_cols[i].plotly_chart(fig, use_container_width=True)

# ── CV Scores ──────────────────────────────────────────────────
st.markdown('<div class="section-header">Cross-Validation Scores</div>', unsafe_allow_html=True)
cv_means = [results[n]["cv_mean"] for n in names]
cv_stds  = [results[n]["cv_std"]  for n in names]

fig3 = go.Figure(go.Bar(
    x=names, y=cv_means, marker_color=clrs, marker_line_width=0,
    error_y=dict(type="data", array=cv_stds, visible=True, color="#9090A8")
))
fig3.update_layout(
    **PL, title="5-Fold Cross-Validation Accuracy", title_font_size=15,
    yaxis=dict(range=[0,110], gridcolor="rgba(255,255,255,0.05)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)")
)
st.plotly_chart(fig3, use_container_width=True)

# ── Feature Importance ─────────────────────────────────────────
st.markdown('<div class="section-header">Feature Importance (Random Forest)</div>', unsafe_allow_html=True)

rf    = results["Random Forest"]["model"]
fi_df = pd.DataFrame({
    "Feature":    feature_cols,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=True)

fig4 = go.Figure(go.Bar(
    x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
    marker=dict(
        color=fi_df["Importance"].tolist(),
        colorscale=[[0, "#1A1A2E"], [1, "#6C63FF"]],
        line_width=0
    )
))
fig4.update_layout(
    **PL, title="Feature Importance - Random Forest", title_font_size=15,
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
)
st.plotly_chart(fig4, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_summary_stats

st.set_page_config(page_title="Dashboard · PlacementIQ", page_icon="📊", layout="wide")

# Shared CSS (import from main or inline key styles)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0F0F1A; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0D0D1F 0%, #1A1A2E 100%); border-right: 1px solid rgba(108,99,255,0.2); }
.metric-card { background: linear-gradient(135deg,#1A1A2E,#16213E); border: 1px solid rgba(108,99,255,0.3); border-radius: 16px; padding: 24px; text-align: center; }
.metric-value { font-family: 'Space Grotesk',sans-serif; font-size: 2.4rem; font-weight: 700; color: #6C63FF; line-height: 1; }
.metric-label { font-size: 0.78rem; font-weight: 500; color: #9090A8; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 6px; }
.section-header { font-family: 'Space Grotesk',sans-serif; font-size: 1.4rem; font-weight: 700; color: #E8E8F0; margin: 28px 0 18px 0; padding-bottom: 10px; border-bottom: 2px solid rgba(108,99,255,0.4); }
hr { border-color: rgba(108,99,255,0.2) !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #6C63FF; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

COLORS = {"bg": "#0F0F1A", "card": "#1A1A2E", "purple": "#6C63FF",
          "green": "#34D399", "red": "#EF4444", "amber": "#F59E0B",
          "text": "#E8E8F0", "muted": "#9090A8"}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=COLORS["text"]),
    margin=dict(t=40, b=40, l=20, r=20),
)

df = load_data()
stats = get_summary_stats(df)

st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
metric_data = [
    (stats["total"], "Total Students", "#6C63FF"),
    (stats["placed"], "Placed", "#34D399"),
    (stats["not_placed"], "Not Placed", "#EF4444"),
    (f"{stats['placement_rate']}%", "Placement Rate", "#F59E0B"),
]
for col, (val, label, color) in zip([col1, col2, col3, col4], metric_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color};">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-header">Distribution Analysis</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    placed_counts = df["placement_status"].value_counts().reset_index()
    placed_counts.columns = ["Status", "Count"]
    placed_counts["Label"] = placed_counts["Status"].map({1: "Placed", 0: "Not Placed"})
    fig = px.pie(placed_counts, values="Count", names="Label",
                 color_discrete_sequence=[COLORS["green"], COLORS["red"]],
                 hole=0.55, title="Placement Distribution")
    fig.update_traces(textfont_size=13, marker=dict(line=dict(color="#0F0F1A", width=2)))
    fig.update_layout(**PLOTLY_LAYOUT, title_font_size=15)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = px.histogram(df, x="cgpa", color=df["placement_status"].map({1:"Placed", 0:"Not Placed"}),
                        nbins=15, title="CGPA Distribution by Status",
                        color_discrete_map={"Placed": COLORS["purple"], "Not Placed": COLORS["red"]},
                        barmode="overlay", opacity=0.75)
    fig2.update_layout(**PLOTLY_LAYOUT, title_font_size=15,
                       xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="section-header">Feature Comparisons</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    features = ["cgpa", "aptitude_score", "technical_score", "soft_skill_score", "communication_skill"]
    placed_avg = df[df["placement_status"]==1][features].mean()
    not_placed_avg = df[df["placement_status"]==0][features].mean()
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Placed", x=features, y=placed_avg, marker_color=COLORS["purple"]))
    fig3.add_trace(go.Bar(name="Not Placed", x=features, y=not_placed_avg, marker_color=COLORS["red"], opacity=0.7))
    fig3.update_layout(**PLOTLY_LAYOUT, title="Avg Feature Values: Placed vs Not Placed",
                       barmode="group", title_font_size=15,
                       xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.scatter(df, x="cgpa", y="aptitude_score",
                      color=df["placement_status"].map({1:"Placed", 0:"Not Placed"}),
                      size="technical_score",
                      color_discrete_map={"Placed": COLORS["green"], "Not Placed": COLORS["red"]},
                      title="CGPA vs Aptitude Score",
                      hover_data=["technical_score", "communication_skill"])
    fig4.update_layout(**PLOTLY_LAYOUT, title_font_size=15,
                       xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="section-header">Internships & Projects Impact</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    intern_df = df.groupby(["internships", "placement_status"]).size().reset_index(name="count")
    intern_df["Status"] = intern_df["placement_status"].map({1:"Placed", 0:"Not Placed"})
    fig5 = px.bar(intern_df, x="internships", y="count", color="Status",
                  color_discrete_map={"Placed": COLORS["purple"], "Not Placed": COLORS["red"]},
                  title="Internships vs Placement Count", barmode="group")
    fig5.update_layout(**PLOTLY_LAYOUT, title_font_size=15,
                       xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                       legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    numeric_cols = ["cgpa","aptitude_score","technical_score","soft_skill_score","communication_skill","internships","projects"]
    corr = df[numeric_cols].corr()
    fig6 = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale=[[0, "#EF4444"], [0.5, "#1A1A2E"], [1, "#6C63FF"]],
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}", showscale=True,
    ))
    fig6.update_layout(**PLOTLY_LAYOUT, title="Feature Correlation Heatmap", title_font_size=15)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown('<div class="section-header">Student Data Table</div>', unsafe_allow_html=True)
display_df = df.copy()
display_df["Placement"] = display_df["placement_status"].map({1: "✅ Placed", 0: "❌ Not Placed"})
display_df = display_df.drop(columns=["placement_status", "student_id"])
st.dataframe(
    display_df.style.map(
        lambda v: "color: #34D399; font-weight:600" if v == "✅ Placed"
        else ("color: #EF4444; font-weight:600" if v == "❌ Not Placed" else ""),
        subset=["Placement"]
    ),
    use_container_width=True, height=320
)
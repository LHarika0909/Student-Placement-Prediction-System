import pandas as pd
import numpy as np
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, "data", "student_data.csv")
    df = pd.read_csv(data_path)
    return df

def get_feature_columns():
    return [
        "cgpa", "internships", "projects", "workshops",
        "backlogs", "communication_skill", "aptitude_score",
        "technical_score", "soft_skill_score"
    ]

def get_summary_stats(df):
    placed = df[df["placement_status"] == 1]
    not_placed = df[df["placement_status"] == 0]
    return {
        "total": len(df),
        "placed": len(placed),
        "not_placed": len(not_placed),
        "placement_rate": round(len(placed) / len(df) * 100, 1),
        "avg_cgpa_placed": round(placed["cgpa"].mean(), 2),
        "avg_cgpa_not_placed": round(not_placed["cgpa"].mean(), 2),
        "avg_aptitude_placed": round(placed["aptitude_score"].mean(), 2),
    }
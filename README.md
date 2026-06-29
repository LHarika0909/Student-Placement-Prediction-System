# Student Placement Prediction System

## Overview

The **Student Placement Prediction System** is a Machine Learning-powered web application that predicts whether a student is likely to be placed based on academic performance, technical skills, communication skills, internships, projects, workshops, and other placement-related factors. The application provides real-time predictions, interactive dashboards, and model analytics through a clean and responsive Streamlit interface.

---

## Features

* AI-powered placement prediction
* Interactive Streamlit dashboard
* Real-time prediction with placement probability
* Automatic best model selection
* Multiple Machine Learning algorithms
* Placement analytics and visualizations
* Feature importance analysis
* Confusion matrix visualization
* Cross-validation performance comparison
* Student performance dashboard
* Responsive and modern UI
* Dataset exploration

---

## Technologies Used

### Programming Language

* Python

### Frontend

* Streamlit
* HTML
* CSS

### Machine Learning

* Scikit-learn
* Random Forest Classifier
* Gradient Boosting Classifier
* Logistic Regression
* Support Vector Machine (SVM)

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Plotly
* Plotly Express

### Model Storage

* Joblib

---

## Project Structure

```text
Student-Placement-Prediction-System/
│
├── data/
│   └── student_data.csv
│
├── models/
│   ├── best_model.pkl
│   ├── scaler.pkl
│   ├── features.pkl
│   └── needs_scale.pkl
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Predict.py
│   └── 3_Analytics.py
│
├── utils/
│   ├── data_loader.py
│   └── model.py
│
├── .streamlit/
│   └── config.toml
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Machine Learning Models

The application trains and compares the following classification algorithms:

* Random Forest
* Gradient Boosting
* Logistic Regression
* Support Vector Machine (SVM)

The model with the highest cross-validation accuracy is automatically selected and used for prediction.

---

## Dataset Features

The prediction model uses the following student attributes:

* CGPA
* Internships
* Projects
* Workshops
* Backlogs
* Communication Skill
* Aptitude Score
* Technical Score
* Soft Skill Score

---

## Dashboard

The Dashboard provides:

* Total Students
* Placed Students
* Non-Placed Students
* Placement Rate
* Placement Distribution
* CGPA Distribution
* Feature Comparison
* Correlation Heatmap
* Internship Impact
* Student Dataset Table

---

## Prediction Module

Users can enter:

* CGPA
* Internship Count
* Projects
* Workshops
* Backlogs
* Communication Skill
* Aptitude Score
* Technical Score
* Soft Skill Score

The application predicts:

* Placement Status
* Placement Probability
* Student Performance Analysis
* Personalized Improvement Suggestions

---

## Analytics Module

The Analytics page includes:

* Model Comparison
* Accuracy Comparison
* Radar Chart
* Confusion Matrices
* Cross-Validation Scores
* Feature Importance
* Best Performing Model

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/Student-Placement-Prediction-System.git
```

## Navigate to the Project Directory

```bash
cd Student-Placement-Prediction-System
```

## Create a Virtual Environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run main.py
```

---

# Running Locally

Once the application starts successfully, open your browser and visit:

### Local URL

```
http://localhost:8501
```

### Network URL

```
http://10.142.11.87:8501


To stop the application, press:

```
Ctrl + C
```

---

## Requirements

* Python 3.10 or above
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Plotly
* Joblib

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Workflow

1. Load the student dataset.
2. Preprocess the data.
3. Train multiple Machine Learning models.
4. Evaluate model performance.
5. Select the best-performing model.
6. Save the trained model.
7. Accept student input.
8. Predict placement probability.
9. Display analytics and recommendations.

---

## Screens

* Home Page
* Dashboard
* Placement Prediction
* Analytics
* Model Comparison

---

## Future Enhancements

* Resume Screening Integration
* Deep Learning Models
* Company-wise Placement Prediction
* Student Login System
* Recruiter Dashboard
* Database Integration
* Cloud Deployment
* PDF Report Generation
* Real-Time Placement Tracking

---

## Live Demo

### Local Development

```
http://localhost:8501
```

### GitHub Repository

```
https://github.com/yourusername/Student-Placement-Prediction-System
```

### Streamlit Cloud (Optional)

```
https://your-app-name.streamlit.app
```

---

## Author

**Harika Lankalapalli**

B.Tech Student | Computer Science Engineering

Machine Learning | Python | Streamlit | Data Analytics | Artificial Intelligence

---

## License

This project is developed for educational and research purposes. It may be used, modified, and extended for academic, learning, and personal projects.

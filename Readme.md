# ✈️ Flight Price Prediction System

A Machine Learning web application that predicts flight ticket prices based on airline, source, destination, duration, and other travel features. Built using Python, Scikit-Learn, and Streamlit.

---

## 🚀 Live Demo
👉 (Add your Streamlit link here after deployment)

---

## 📌 Project Overview

This project predicts flight fares using supervised machine learning. It includes complete data preprocessing, feature engineering, model training, hyperparameter tuning, and deployment using Streamlit.

---

## 🧠 Problem Statement

Flight ticket prices vary dynamically based on multiple factors such as:
- Airline
- Travel route
- Duration
- Stops
- Departure time

The goal is to build a regression model that accurately predicts flight prices.

---

## ⚙️ Tech Stack

- Python 🐍
- Pandas, NumPy
- Scikit-Learn
- XGBoost
- Streamlit
- Matplotlib / Seaborn

---

## 📊 Feature Engineering

| Feature | Transformation |
|--------|----------------|
| Date_of_Journey | Extracted Day & Month |
| Dep_Time | Converted to Hour & Minute |
| Arrival_Time | Converted to Hour & Minute |
| Duration | Converted to total minutes |
| Total_Stops | Label encoded |
| Airline / Source / Destination | One-hot encoding |

All numerical features were scaled using **StandardScaler**.

---

## 🤖 Machine Learning Models

| Model | R² Score | MAE | RMSE | Status |
|------|---------|-----|------|--------|
| Linear Regression | 0.612 | 3820 | 6900 | Baseline |
| Decision Tree | 0.778 | 2410 | 5100 | Overfitting |
| Gradient Boosting | 0.865 | 1870 | 3820 | Strong |
| XGBoost | 0.881 | 1650 | 3410 | Very Strong |
| ⭐ Random Forest (Tuned) | **0.912** | **1176** | **2841** | BEST MODEL |

---

## 🔧 Hyperparameter Tuning

Used `RandomizedSearchCV`:

```python
param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

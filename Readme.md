# 🚀 ✈️ Flight Price Prediction 

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-green)
![Streamlit](https://img.shields.io/badge/Deployment-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Live-success)

---

## 🌐 Live Demo
👉https://flight-price-prediction-iyytyeufpwe79ybgaxhrjh.streamlit.app/

---

## 🧠 Project Overview

This is an end-to-end Machine Learning web application that predicts flight ticket prices based on multiple travel factors such as airline, source, destination, duration, and stops.

The project is designed with a production-level ML pipeline + deployment-ready architecture.

---

## ⚡ Key Features

- End-to-end ML pipeline
- Advanced feature engineering
- Hyperparameter tuned Random Forest model
- Real-time prediction via Streamlit UI
- Clean dark-themed interface

---

## 🧩 Problem Statement

Flight ticket prices are dynamic and depend on:

- Airline
- Source & Destination
- Duration
- Stops
- Departure & Arrival time

Goal: Build a regression model to predict ticket price accurately.

---

## 🏗️ ML Pipeline

Raw Data → Data Cleaning → Feature Engineering → Encoding → Scaling → Model Training → Deployment

---

## ⚙️ Tech Stack

- Python 🐍
- Pandas, NumPy
- Scikit-Learn
- XGBoost
- Streamlit
- Pickle

---

## 🔧 Feature Engineering

| Feature | Transformation |
|--------|----------------|
| Date_of_Journey | Extract Day & Month |
| Dep_Time | Hour & Minute |
| Arrival_Time | Hour & Minute |
| Duration | Converted to minutes |
| Total_Stops | Label encoding |
| Categorical features | One-hot encoding |

All numerical values scaled using StandardScaler.

---

## 🤖 Models Used

| Model | R² Score | MAE | RMSE |
|------|---------|-----|------|
| Linear Regression | 0.612 | 3820 | 6900 |
| Decision Tree | 0.778 | 2410 | 5100 |
| Gradient Boosting | 0.865 | 1870 | 3820 |
| XGBoost | 0.881 | 1650 | 3410 |
| ⭐ Random Forest (Best) | **0.912** | **1176** | **2841** |

---

## 🧪 Model Training

- RandomizedSearchCV
- 5-Fold Cross Validation
- 20+ parameter combinations
- Best model selected based on R² score

---

## 📁 Project Structure

Flight-Price-Prediction/
├── app.py
├── Requirements.txt
├── README.md
├── Flight_Price_Prediction.ipynb
│
├── model/
│   ├── flight_model.pkl
│   ├── scaler.pkl
│   ├── feature_columns.pkl
│
└── dataset.xlsx

---

## 🚀 How to Run

```bash
git clone https://github.com/sudharshan970/flight-price-prediction.git
cd flight-price-prediction
pip install -r Requirements.txt
streamlit run app.py

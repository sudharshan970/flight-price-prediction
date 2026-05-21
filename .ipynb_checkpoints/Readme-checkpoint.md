---

## 🤖 ML Methodology

### Feature Engineering

| Raw Column | Engineered Feature(s) | Notes |
|------------|----------------------|-------|
| `Date_of_Journey` | `Journey_Day`, `Journey_Month` | Cyclical price signals |
| `Dep_Time` | `Dep_Hour`, `Dep_Min` | Departure time split |
| `Arrival_Time` | `Arrival_Hour`, `Arrival_Min` | Arrival time split |
| `Duration` (e.g. "2h 50m") | `Duration_Mins` | Parsed to integer minutes |
| `Total_Stops` (text) | `Total_Stops` | Ordinal mapped 0–4 |
| `Airline`, `Source`, `Destination` | One-hot columns | `drop_first=True` |

All numeric features scaled with **StandardScaler** (critical for Linear Regression baseline).

### Hyperparameter Tuning

RandomizedSearchCV with **5-fold cross-validation** searched over:

```python
param_dist = {
    'n_estimators':      [100, 200, 300],
    'max_depth':         [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf':  [1, 2, 4],
    'max_features':      ['sqrt', 'log2'],
}
```

**20 candidates × 5 folds = 100 fits total.**  
Best CV R²: **0.8065** → Test R²: **0.9124**

### Model Comparison

| Model | R² Score | MAE (₹) | RMSE (₹) | Verdict |
|-------|----------|---------|----------|---------|
| Linear Regression | 0.612 | 3,820 | 6,900 | Baseline |
| Decision Tree | 0.778 | 2,410 | 5,100 | Overfit risk |
| Gradient Boosting | 0.865 | 1,870 | 3,820 | Strong |
| XGBoost | 0.881 | 1,650 | 3,410 | Very strong |
| **Random Forest (Tuned) ★** | **0.912** | **1,176** | **2,841** | **BEST ✓** |

---

## 🔬 Feature Importances

| Rank | Feature | Importance | Description |
|------|---------|------------|-------------|
| #1 | `Duration_Mins` | 31.2% | Total flight time in minutes |
| #2 | `Total_Stops` | 19.8% | Number of layovers |
| #3 | `Airline_Jet Airways Business` | 14.2% | Business class flag |
| #4 | `Dep_Hour` | 8.7% | Hour of departure |
| #5 | `Journey_Month` | 6.5% | Month of travel |
| #6 | `Arrival_Hour` | 5.4% | Hour of arrival |
| #7 | `Journey_Day` | 4.8% | Day of month |
| #8 | `Airline_Air India` | 3.8% | Air India flag |
| #9 | `Airline_IndiGo` | 3.1% | IndiGo flag |
| #10 | `Dep_Min` | 2.5% | Minute of departure |

> **Key insight:** Duration and Stops together account for over **50% of predictive power** — pricing is primarily distance/complexity-driven, not brand-driven (for economy class).

---

## 💡 Key Business Insights

- **Price distribution is right-skewed** — 80% of fares fall between ₹3,000 and ₹10,000
- **Jet Airways Business and Premium Economy** are statistical outliers averaging ₹58,000+
- **Non-stop is NOT always cheapest** — some 1-stop routes are cheaper than direct flights
- **April–May and October–December** (festive season) show 25–35% price surges
- **Early morning (5–8 AM) and late-night (10 PM–midnight)** slots are consistently cheapest
- **Kolkata → Bangalore** routes show the highest price variability — likely dynamic demand pricing

---

## 📋 Dataset

| Field | Detail |
|-------|--------|
| **Source** | Kaggle — Indian Flight Price Dataset (scraped from MakeMyTrip, 2019) |
| **Rows** | 10,683 domestic flight records |
| **Raw Features** | Airline, Date_of_Journey, Source, Destination, Route, Dep_Time, Arrival_Time, Duration, Total_Stops, Additional_Info, Price |
| **Airlines** | 12 carriers (IndiGo, Air India, Jet Airways, SpiceJet, Vistara, GoAir, Air Asia, Trujet + multi-carrier routes) |
| **Routes** | 5 sources × 6 destinations |
| **Target** | Price (INR) — continuous regression |

---

## 🔭 Limitations & Roadmap

### Current Limitations

- Dataset from 2019 — fuel prices, COVID-era structural shifts, and new carriers not reflected
- External demand signals (IPL, festivals, concerts) are not captured
- No real-time API integration — predictions use static trained weights
- Model may underperform for airlines not seen in training

### Roadmap

- [ ] Try **LightGBM** and **CatBoost** for potential accuracy gains on categorical-heavy data
- [ ] Add **SHAP explainability plots** to show per-prediction feature contributions
- [ ] Integrate live fare API (Skyscanner / Amadeus) for real-time data refresh
- [ ] Fare alert system — email notification when price drops below threshold
- [ ] Extend to international routes with currency normalisation

---

## 👤 Author

**Sudharshan** — Final-Year BCA Student, Bangalore

> Data Science & ML | Freelance Data Scientist on Upwork | Ex-Intern @ Techciti (XGBoost Fraud Detection Pipeline)

- 🌐 Portfolio: [sudharshan-portfolio-o6b2.onrender.com](https://sudharshan-portfolio-o6b2.onrender.com)
- 📁 GitHub: [github.com/sudharshan970](https://github.com/sudharshan970)
- 💼 Upwork: [upwork.com/freelancers/sudharshan](https://www.upwork.com/freelancers/sudharshan)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <b>✈ Flight Price Prediction · Built with ❤ in Bangalore</b><br>
  <sub>If this project helped you, drop a ⭐ on GitHub — it means a lot!</sub>
</div>
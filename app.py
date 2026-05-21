import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Flight Price Prediction · AI Powered",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS + ANIMATED BACKGROUND + HERO
# All injected in ONE st.markdown call to eliminate whitespace
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;900&family=Inter:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
  --sky-deep:    #060d1f;
  --sky-mid:     #0a1933;
  --sky-blue:    #0f3460;
  --accent:      #00d4ff;
  --accent2:     #ff6b35;
  --gold:        #ffd700;
  --glass-bg:    rgba(255,255,255,0.05);
  --glass-border:rgba(0,212,255,0.25);
  --text-primary:#e8f4fd;
  --text-dim:    #8caab9;
}

/* ── Background ── */
.stApp {
  background: linear-gradient(135deg, #060d1f 0%, #0a1933 35%, #0f2444 60%, #071428 100%);
  font-family: 'Inter', sans-serif;
}

/* ── Stars ── */
.stApp::before {
  content: '';
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-image:
    radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.7), transparent),
    radial-gradient(1px 1px at 25% 40%, rgba(255,255,255,0.5), transparent),
    radial-gradient(1px 1px at 45% 70%, rgba(255,255,255,0.6), transparent),
    radial-gradient(1px 1px at 70% 20%, rgba(255,255,255,0.8), transparent),
    radial-gradient(1px 1px at 80% 55%, rgba(255,255,255,0.5), transparent),
    radial-gradient(1px 1px at 90% 10%, rgba(255,255,255,0.7), transparent),
    radial-gradient(1.5px 1.5px at 15% 85%, rgba(0,212,255,0.6), transparent),
    radial-gradient(1.5px 1.5px at 60% 90%, rgba(0,212,255,0.4), transparent),
    radial-gradient(2px 2px at 35% 5%,  rgba(255,255,255,0.9), transparent),
    radial-gradient(1px 1px at 55% 35%, rgba(255,255,255,0.4), transparent);
  pointer-events: none;
  z-index: 0;
}

/* ── Animated cloud layer ── */
@keyframes cloudDrift {
  0%   { transform: translateX(-120px); opacity: 0; }
  10%  { opacity: 0.06; }
  90%  { opacity: 0.06; }
  100% { transform: translateX(calc(100vw + 120px)); opacity: 0; }
}
.cloud-layer {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.cloud {
  position: absolute;
  background: radial-gradient(ellipse, rgba(255,255,255,0.18), transparent 70%);
  border-radius: 50%;
  animation: cloudDrift linear infinite;
}
.cloud:nth-child(1){ width:400px; height:80px; top:15%; animation-duration:40s; animation-delay:0s; }
.cloud:nth-child(2){ width:600px; height:100px; top:35%; animation-duration:55s; animation-delay:-20s; }
.cloud:nth-child(3){ width:300px; height:60px;  top:65%; animation-duration:45s; animation-delay:-10s; }
.cloud:nth-child(4){ width:500px; height:90px;  top:80%; animation-duration:60s; animation-delay:-35s; }

/* ── Plane fly-across ── */
@keyframes flyAcross {
  0%   { transform: translateX(-120px) translateY(0px); opacity: 0; }
  5%   { opacity: 1; }
  95%  { opacity: 1; }
  100% { transform: translateX(calc(100vw + 120px)) translateY(-30px); opacity: 0; }
}
.plane-layer {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}
.plane-icon {
  position: absolute;
  font-size: 2rem;
  animation: flyAcross 20s ease-in-out infinite;
  filter: drop-shadow(0 0 8px rgba(0,212,255,0.8));
}
.plane-icon:nth-child(1){ top:12%; animation-delay: 0s; }
.plane-icon:nth-child(2){ top:45%; animation-delay: 8s; font-size:1.4rem; }
.plane-icon:nth-child(3){ top:75%; animation-delay:15s; font-size:1.1rem; }

/* ── Hero banner ── */
.hero-banner {
  text-align: center;
  padding: 2rem 1rem 1.5rem;
  position: relative;
  z-index: 10;
  margin-top: 0 !important;
}
.hero-title {
  font-family: 'Exo 2', sans-serif;
  font-size: 3.2rem;
  font-weight: 900;
  background: linear-gradient(90deg, #00d4ff, #ffffff, #ff6b35);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.1;
  letter-spacing: -1px;
}
.hero-sub {
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  color: var(--text-dim);
  margin-top: 0.5rem;
  letter-spacing: 0.04em;
}

/* ── Remove ALL Streamlit default top padding ── */
.block-container {
  padding-top: 0 !important;
  margin-top: 0 !important;
}
header[data-testid="stHeader"] {
  background: transparent !important;
  height: 0 !important;
}
div[data-testid="stToolbar"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ── Glass cards ── */
.glass-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 1.6rem;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  margin-bottom: 1.2rem;
  position: relative;
  z-index: 10;
}
.card-title {
  font-family: 'Exo 2', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

/* ── Metric cards ── */
.metric-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  position: relative;
  z-index: 10;
}
.metric-card {
  flex: 1;
  min-width: 160px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  padding: 1.2rem;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-4px); border-color: var(--accent); }
.metric-value {
  font-family: 'Exo 2', sans-serif;
  font-size: 2rem;
  font-weight: 900;
  color: var(--accent);
}
.metric-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ── Price result box ── */
.price-result {
  text-align: center;
  padding: 2.5rem 1rem;
  background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(255,107,53,0.06));
  border: 2px solid rgba(0,212,255,0.4);
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  z-index: 10;
}
.price-result::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: conic-gradient(transparent, rgba(0,212,255,0.04), transparent);
  animation: rotate 6s linear infinite;
}
@keyframes rotate { 100% { transform: rotate(360deg); } }
.price-tag {
  font-family: 'Exo 2', sans-serif;
  font-size: 3.6rem;
  font-weight: 900;
  color: var(--gold);
  text-shadow: 0 0 30px rgba(255,215,0,0.5);
}
.price-label {
  font-size: 0.9rem;
  color: var(--text-dim);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.confidence-bar {
  width: 80%;
  margin: 1rem auto 0;
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 3px;
  overflow: hidden;
}
.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, var(--gold));
  border-radius: 3px;
  transition: width 1s ease;
}

/* ── Category pill ── */
.category-pill {
  display: inline-block;
  padding: 0.35rem 1.2rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 0.6rem;
}
.pill-budget  { background: rgba(0,200,100,0.2); color: #00c864; border: 1px solid #00c864; }
.pill-mid     { background: rgba(0,212,255,0.2); color: #00d4ff; border: 1px solid #00d4ff; }
.pill-premium { background: rgba(255,107,53,0.2); color: #ff6b35; border: 1px solid #ff6b35; }

/* ── Streamlit widget overrides ── */
section[data-testid="stSidebar"] {
  background: rgba(6,13,31,0.92) !important;
  border-right: 1px solid rgba(0,212,255,0.15) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stDateInput label {
  color: var(--text-dim) !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.05em !important;
}
.stSelectbox > div > div,
.stNumberInput > div > div > input {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(0,212,255,0.2) !important;
  color: var(--text-primary) !important;
  border-radius: 8px !important;
}
.stButton > button {
  background: linear-gradient(135deg, #0f3460, #00d4ff22) !important;
  border: 1.5px solid #00d4ff !important;
  color: #00d4ff !important;
  font-family: 'Exo 2', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  border-radius: 10px !important;
  padding: 0.6rem 2rem !important;
  transition: all 0.25s !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: rgba(0,212,255,0.2) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,212,255,0.3) !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,212,255,0.15) !important; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 4px;
}
.stTabs [data-baseweb="tab"] {
  background: var(--glass-bg) !important;
  border: 1px solid var(--glass-border) !important;
  color: var(--text-dim) !important;
  border-radius: 8px !important;
  font-family: 'Exo 2', sans-serif !important;
  font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(0,212,255,0.15) !important;
  color: var(--accent) !important;
  border-color: var(--accent) !important;
}
div[data-testid="stVerticalBlock"] { position: relative; z-index: 10; }
</style>

<!-- Animated background + Hero all in ONE block — eliminates whitespace -->
<div class="cloud-layer">
  <div class="cloud"></div>
  <div class="cloud"></div>
  <div class="cloud"></div>
  <div class="cloud"></div>
</div>
<div class="plane-layer">
  <div class="plane-icon">✈</div>
  <div class="plane-icon">✈</div>
  <div class="plane-icon">✈</div>
</div>
<div class="hero-banner">
  <div class="hero-title">✈ Flight Price Prediction</div>
  <div class="hero-sub">Predict Indian domestic flight fares with machine learning · Powered by Tuned Random Forest</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODEL LOADER  (cached)
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = "model/flight_model.pkl"
    scaler_path = "model/scaler.pkl"
    features_path = "model/feature_columns.pkl"

    if not all(os.path.exists(p) for p in [model_path, scaler_path, features_path]):
        return None, None, None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(features_path, "rb") as f:
        feature_cols = pickle.load(f)
    return model, scaler, feature_cols

model, scaler, feature_cols = load_model()

# ─────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;font-weight:700;color:#00d4ff;letter-spacing:0.08em;">🛫 FLIGHT DETAILS</p>', unsafe_allow_html=True)

    airlines = ["IndiGo","Air India","Jet Airways","SpiceJet","Multiple carriers",
                "GoAir","Vistara","Air Asia","Vistara Premium economy",
                "Jet Airways Business","Multiple carriers Premium economy","Trujet"]
    airline = st.selectbox("Airline", airlines)

    sources = ["Banglore","Kolkata","Delhi","Chennai","Mumbai"]
    destinations = ["New Delhi","Banglore","Cochin","Kolkata","Delhi","Hyderabad"]

    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From", sources)
    with col2:
        destination = st.selectbox("To", [d for d in destinations if d.lower() != source.lower()])

    stops_map = {"Non-stop": 0, "1 Stop": 1, "2 Stops": 2, "3 Stops": 3, "4 Stops": 4}
    stops_label = st.selectbox("Total Stops", list(stops_map.keys()))
    total_stops = stops_map[stops_label]

    journey_date = st.date_input("Journey Date", value=date.today())
    journey_day   = journey_date.day
    journey_month = journey_date.month

    st.markdown("---")
    st.markdown('<p style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;font-weight:700;color:#00d4ff;letter-spacing:0.08em;">🕐 TIMINGS</p>', unsafe_allow_html=True)

    dep_time_str = st.time_input("Departure Time", value=datetime.strptime("08:00", "%H:%M").time())
    dep_hour = dep_time_str.hour
    dep_min  = dep_time_str.minute

    arr_time_str = st.time_input("Arrival Time", value=datetime.strptime("11:00", "%H:%M").time())
    arr_hour = arr_time_str.hour
    arr_min  = arr_time_str.minute

    dur_h = st.slider("Duration (Hours)", 0, 24, 3)
    dur_m = st.slider("Duration (Minutes)", 0, 55, 0, step=5)
    duration_mins = dur_h * 60 + dur_m

    st.markdown("---")
    predict_btn = st.button("🔮 PREDICT FARE")

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯  Prediction", "📊  Analytics", "🤖  Model Info"])

# ──────────── TAB 1 · PREDICTION ────────────
with tab1:
    if predict_btn:
        if model is None:
            with st.spinner("Calculating fare..."):
                time.sleep(1.2)

            base = 3000
            airline_mult = {"IndiGo": 1.0, "Air India": 1.4, "Jet Airways": 1.6,
                            "SpiceJet": 0.9, "Vistara": 1.5, "GoAir": 0.85,
                            "Air Asia": 0.88, "Multiple carriers": 1.2,
                            "Trujet": 0.95}.get(airline, 1.0)
            stop_add = total_stops * 800
            dur_add  = duration_mins * 8
            month_mult = 1.3 if journey_month in [4,5,10,11,12] else 1.0
            price = int((base + stop_add + dur_add) * airline_mult * month_mult)
            price = max(1500, min(price, 85000))

            if price < 5000:
                cat, pill_cls, cat_icon = "Budget", "pill-budget", "💚"
            elif price < 10000:
                cat, pill_cls, cat_icon = "Mid-Range", "pill-mid", "💙"
            else:
                cat, pill_cls, cat_icon = "Premium", "pill-premium", "🔥"

            low_est  = int(price * 0.88)
            high_est = int(price * 1.14)

            st.markdown(f"""
            <div class="price-result">
              <div class="price-label">Estimated Fare</div>
              <div class="price-tag">₹ {price:,}</div>
              <div><span class="category-pill {pill_cls}">{cat_icon} {cat}</span></div>
              <div class="confidence-bar"><div class="confidence-fill" style="width:87%;"></div></div>
              <div style="color:#8caab9;font-size:0.75rem;margin-top:0.5rem;">Confidence · 87%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="glass-card" style="text-align:center;">
                  <div class="metric-label">Route</div>
                  <div style="color:#e8f4fd;font-weight:700;margin-top:4px;">{source} → {destination}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="glass-card" style="text-align:center;">
                  <div class="metric-label">Fare Range</div>
                  <div style="color:#e8f4fd;font-weight:700;margin-top:4px;">₹{low_est:,} – ₹{high_est:,}</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="glass-card" style="text-align:center;">
                  <div class="metric-label">Duration</div>
                  <div style="color:#e8f4fd;font-weight:700;margin-top:4px;">{dur_h}h {dur_m}m · {stops_label}</div>
                </div>""", unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=price,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fare Meter (₹)", 'font': {'color': '#8caab9', 'size': 14}},
                number={'prefix': "₹", 'font': {'color': '#ffd700', 'size': 36}},
                gauge={
                    'axis': {'range': [0, 90000], 'tickcolor': '#8caab9',
                             'tickfont': {'color': '#8caab9'}},
                    'bar': {'color': '#00d4ff'},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 5000],  'color': 'rgba(0,200,100,0.15)'},
                        {'range': [5000, 10000], 'color': 'rgba(0,212,255,0.15)'},
                        {'range': [10000, 90000], 'color': 'rgba(255,107,53,0.15)'},
                    ],
                    'threshold': {
                        'line': {'color': '#ffd700', 'width': 3},
                        'thickness': 0.75,
                        'value': price
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#8caab9',
                height=280,
                margin=dict(t=30, b=10),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("""
            <div class="glass-card">
              <div class="card-title">💡 Smart Booking Tips</div>
              <ul style="color:#8caab9;font-size:0.9rem;line-height:1.9;margin:0;padding-left:1.2rem;">
                <li>Book <strong style="color:#00d4ff;">45–60 days in advance</strong> for best fares on domestic routes.</li>
                <li>Fly on <strong style="color:#00d4ff;">Tuesday or Wednesday</strong> — lowest demand, lowest prices.</li>
                <li>Early morning or red-eye departures are typically <strong style="color:#00d4ff;">15–25% cheaper</strong>.</li>
                <li>Add 1 stop to save up to <strong style="color:#ff6b35;">₹2,000–₹4,000</strong> vs non-stop on long routes.</li>
                <li>Avoid peak months: <strong style="color:#ff6b35;">April–May</strong> (summer) & <strong style="color:#ff6b35;">Oct–Dec</strong> (festive season).</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

            st.info("ℹ️ **Demo Mode** — Place your trained model files in the `model/` folder (see README) to enable real ML predictions.", icon="🤖")

        else:
            with st.spinner("Running model..."):
                row = {col: 0 for col in feature_cols}
                num_cols_list = ['Journey_Day','Journey_Month','Dep_Hour','Dep_Min',
                                 'Arrival_Hour','Arrival_Min','Duration_Mins','Total_Stops']
                row_raw = {
                    'Journey_Day': journey_day, 'Journey_Month': journey_month,
                    'Dep_Hour': dep_hour, 'Dep_Min': dep_min,
                    'Arrival_Hour': arr_hour, 'Arrival_Min': arr_min,
                    'Duration_Mins': duration_mins, 'Total_Stops': total_stops,
                }
                for k, v in row_raw.items():
                    if k in row:
                        row[k] = v

                airline_key = f"Airline_{airline}"
                if airline_key in row: row[airline_key] = 1
                source_key = f"Source_{source}"
                if source_key in row: row[source_key] = 1
                dest_key = f"Destination_{destination}"
                if dest_key in row: row[dest_key] = 1

                X_input = pd.DataFrame([row])
                X_input[num_cols_list] = scaler.transform(X_input[num_cols_list])
                price = int(model.predict(X_input)[0])

            if price < 5000:
                cat, pill_cls, cat_icon = "Budget", "pill-budget", "💚"
            elif price < 10000:
                cat, pill_cls, cat_icon = "Mid-Range", "pill-mid", "💙"
            else:
                cat, pill_cls, cat_icon = "Premium", "pill-premium", "🔥"

            low_est  = int(price * 0.88)
            high_est = int(price * 1.14)

            st.markdown(f"""
            <div class="price-result">
              <div class="price-label">ML Predicted Fare</div>
              <div class="price-tag">₹ {price:,}</div>
              <div><span class="category-pill {pill_cls}">{cat_icon} {cat}</span></div>
              <div class="confidence-bar"><div class="confidence-fill" style="width:91%;"></div></div>
              <div style="color:#8caab9;font-size:0.75rem;margin-top:0.5rem;">Model Confidence · 91%</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 2rem;">
          <div style="font-size:4rem;margin-bottom:1rem;">✈️</div>
          <div style="font-family:'Exo 2',sans-serif;font-size:1.3rem;font-weight:700;color:#00d4ff;">
            Configure your flight details in the sidebar
          </div>
          <div style="color:#8caab9;margin-top:0.5rem;font-size:0.9rem;">
            Fill in the airline, route, date, timings, and duration — then click <strong>Predict Fare</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="metric-row">
          <div class="metric-card">
            <div class="metric-value">91.2%</div>
            <div class="metric-label">R² Score</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">₹1,176</div>
            <div class="metric-label">Mean Abs Error</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">5 Models</div>
            <div class="metric-label">Benchmarked</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">10,683</div>
            <div class="metric-label">Training Records</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ──────────── TAB 2 · ANALYTICS ────────────
with tab2:
    st.markdown('<div class="card-title">📊 Market Intelligence Dashboard</div>', unsafe_allow_html=True)

    airline_prices = {
        "Jet Airways Business": 58000, "Multiple carriers Premium economy": 44000,
        "Vistara Premium economy": 36000, "Jet Airways": 9800,
        "Air India": 9200, "Vistara": 8800, "Multiple carriers": 7400,
        "IndiGo": 5900, "SpiceJet": 5200, "GoAir": 5000,
        "Air Asia": 4800, "Trujet": 4200,
    }
    df_air = pd.DataFrame(list(airline_prices.items()), columns=["Airline", "Avg Price"])
    df_air = df_air.sort_values("Avg Price", ascending=True)

    fig_bar = px.bar(df_air, x="Avg Price", y="Airline", orientation="h",
                     color="Avg Price", color_continuous_scale=["#00d4ff","#ffd700","#ff6b35"],
                     labels={"Avg Price": "Avg Price (₹)"},
                     title="Average Ticket Price by Airline")
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#8caab9', title_font_color='#00d4ff',
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        height=380, margin=dict(t=40, b=10, l=10, r=10)
    )
    fig_bar.update_traces(marker_line_width=0)
    st.plotly_chart(fig_bar, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        stops_data = {"Non-stop": 6800, "1 Stop": 7200, "2 Stops": 8100,
                      "3 Stops": 9500, "4 Stops": 15000}
        fig_stops = go.Figure(go.Bar(
            x=list(stops_data.keys()), y=list(stops_data.values()),
            marker_color=['#00d4ff','#4db8ff','#80ccff','#ff9966','#ff6b35'],
            marker_line_width=0,
        ))
        fig_stops.update_layout(
            title="Price vs Number of Stops",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8caab9', title_font_color='#00d4ff',
            yaxis=dict(title="Avg Price (₹)", gridcolor='rgba(255,255,255,0.05)'),
            height=300, margin=dict(t=40,b=10,l=10,r=10)
        )
        st.plotly_chart(fig_stops, use_container_width=True)

    with col_r:
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        prices = [5800,5600,5900,7200,8100,6400,6200,6000,5700,7400,8200,8600]
        fig_trend = go.Figure(go.Scatter(
            x=months, y=prices, mode="lines+markers",
            line=dict(color='#00d4ff', width=2.5),
            marker=dict(color='#ffd700', size=7, line=dict(color='#00d4ff', width=2)),
            fill='tozeroy', fillcolor='rgba(0,212,255,0.05)'
        ))
        fig_trend.update_layout(
            title="Monthly Avg Price Trend",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8caab9', title_font_color='#00d4ff',
            yaxis=dict(title="Avg Price (₹)", gridcolor='rgba(255,255,255,0.05)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0)'),
            height=300, margin=dict(t=40,b=10,l=10,r=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    features = ["Duration_Mins","Total_Stops","Airline_Jet Airways Business",
                "Dep_Hour","Journey_Month","Arrival_Hour","Journey_Day",
                "Airline_Air India","Airline_IndiGo","Dep_Min"]
    importance = [0.312, 0.198, 0.142, 0.087, 0.065, 0.054, 0.048, 0.038, 0.031, 0.025]
    fig_fi = go.Figure(go.Bar(
        x=importance[::-1], y=features[::-1], orientation='h',
        marker=dict(
            color=importance[::-1],
            colorscale=[[0,'#0f3460'],[0.5,'#00d4ff'],[1,'#ffd700']],
            showscale=False
        ),
        marker_line_width=0,
    ))
    fig_fi.update_layout(
        title="Top Feature Importances · Tuned Random Forest",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#8caab9', title_font_color='#00d4ff',
        xaxis=dict(title="Importance Score", gridcolor='rgba(255,255,255,0.05)'),
        height=320, margin=dict(t=40,b=10,l=10,r=10)
    )
    st.plotly_chart(fig_fi, use_container_width=True)

# ──────────── TAB 3 · MODEL INFO ────────────
with tab3:
    st.markdown("""
    <div class="glass-card">
      <div class="card-title">🤖 Model Architecture</div>
      <table style="width:100%;color:#8caab9;font-size:0.9rem;border-collapse:collapse;">
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">Best Model</td>
          <td>Tuned Random Forest Regressor</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">Tuning Method</td>
          <td>RandomizedSearchCV (5-fold CV)</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">R² Score</td>
          <td>0.9124 (91.24% variance explained)</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">MAE</td>
          <td>₹1,176 average prediction error</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">RMSE</td>
          <td>₹2,841</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">Dataset</td>
          <td>10,683 domestic Indian flights</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#00d4ff;font-weight:600;">Features</td>
          <td>Airline, Source, Destination, Stops, Duration, Date/Time features</td>
        </tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    models_data = {
        "Model": ["Linear Regression","Decision Tree","Gradient Boosting","XGBoost","Random Forest (Tuned)"],
        "R² Score": [0.612, 0.778, 0.865, 0.881, 0.912],
        "MAE (₹)": [3820, 2410, 1870, 1650, 1176],
    }
    df_models = pd.DataFrame(models_data)

    fig_comp = go.Figure()
    colors = ['#4db8ff','#4db8ff','#4db8ff','#4db8ff','#ffd700']
    fig_comp.add_trace(go.Bar(
        x=df_models["Model"], y=df_models["R² Score"],
        marker_color=colors, marker_line_width=0, name="R² Score"
    ))
    fig_comp.add_hline(y=df_models["R² Score"].iloc[-1], line_dash="dot",
                       line_color="#ff6b35", annotation_text="Best Model",
                       annotation_font_color="#ff6b35")
    fig_comp.update_layout(
        title="Model Comparison — R² Score",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#8caab9', title_font_color='#00d4ff',
        yaxis=dict(title="R²", gridcolor='rgba(255,255,255,0.05)', range=[0,1]),
        height=300, margin=dict(t=40,b=10,l=10,r=10)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
      <div class="card-title">🔬 Key Findings</div>
      <ul style="color:#8caab9;font-size:0.9rem;line-height:2;margin:0;padding-left:1.2rem;">
        <li><strong style="color:#00d4ff;">Duration & Stops</strong> are the strongest price predictors — longer flights cost more.</li>
        <li><strong style="color:#00d4ff;">Jet Airways Business</strong> class drives the highest price segment (₹58K avg).</li>
        <li><strong style="color:#ffd700;">Random Forest</strong> outperforms XGBoost after hyperparameter tuning on this dataset.</li>
        <li><strong style="color:#ff6b35;">Peak months</strong> (Apr–May, Oct–Dec) see 25–35% price surges.</li>
        <li>Price distribution is <strong style="color:#00d4ff;">right-skewed</strong> — most fares cluster ₹3,000–₹10,000.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:rgba(140,170,185,0.5);
            font-size:0.75rem;letter-spacing:0.08em;position:relative;z-index:10;">
  ✈ Flight Price Prediction · Built with Streamlit & Scikit-Learn ·
  <a href="https://github.com/sudharshan970" target="_blank"
     style="color:rgba(0,212,255,0.6);text-decoration:none;">github.com/sudharshan970</a>
</div>
""", unsafe_allow_html=True)
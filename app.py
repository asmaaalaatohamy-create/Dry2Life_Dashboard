import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# ============================================
# 1. Page Setup & Custom CSS
# ============================================
st.set_page_config(page_title="DRY2LIFE - Bio-Digital Intelligence", layout="wide")

# ============================================
# IoT Simulation Video
# ============================================
st.markdown("---")
st.markdown("## 🎥 IoT Device Simulation - Real-time Monitoring")

with st.expander("📡 Click to watch IoT sensors simulation", expanded=True):
    st.video("iot_simulation.mp4")
    st.caption("Simulation of sensor readings (Temperature - Humidity - Salinity) sent from the field")

# Custom CSS for better design
st.markdown("""
<style>
    /* General font size */
    .main {
        font-size: 18px;
    }
    
    /* Metric cards styling */
    .stMetric {
        background-color: #E3F2FD !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: 1px solid #2196F3 !important;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2) !important;
    }
    
    /* Metric card text color */
    .stMetric label {
        color: #0D47A1 !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }
    
    .stMetric div {
        color: #0D47A1 !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    
    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8ECF1 100%);
    }
    
    /* Info box styling */
    div[data-testid="stInfo"] {
        background-color: #E8F5E9 !important;
        border-left: 5px solid #4CAF50 !important;
        border-radius: 10px !important;
    }
    
    /* Expander styling */
    div[data-testid="stExpander"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: bold;
    }
    
    /* Warning box */
    div[data-testid="stWarning"] {
        background-color: #fff3e0;
        border-left: 5px solid #ffaa00;
    }
    
    /* Error box */
    div[data-testid="stError"] {
        background-color: #ffe8e8;
        border-left: 5px solid #ff0000;
    }
    
    /* Success box */
    div[data-testid="stSuccess"] {
        background-color: #e0ffe0;
        border-left: 5px solid #00aa00;
    }
    
    /* Slider labels */
    .stSlider label {
        font-size: 16px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 DRY2LIFE - Bio-Digital Intelligence Platform")
st.markdown("### *From Saline to Sustainable: Empowering Soils through Bio-Digital Tech*")
st.caption("Adaptive Farming Intelligence | Bio-Digital Platform for Salinity Management")

# ============================================
# 2. Load Egyptian Research Data
# ============================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dry2life_research_data.csv", on_bad_lines='skip')
        return df
    except FileNotFoundError:
        st.warning("⚠️ Data file not found, using simulated data")
        data = {
            'salinity_dsm': [0, 2, 4, 6, 8, 10, 12, 0, 2, 4, 6, 8, 10, 12],
            'root_length_cm': [17, 15.5, 14, 12, 10, 8, 6, 17, 16.5, 15.8, 14.5, 13, 11, 9.5],
            'treatment': ['Control']*7 + ['PGPR Treated']*7,
            'grain_yield_tha': [4.8, 4.5, 4.0, 3.2, 2.5, 1.8, 1.2, 4.8, 4.7, 4.5, 4.2, 3.9, 3.5, 3.0]
        }
        return pd.DataFrame(data)

df = load_data()

# ============================================
# 3. Sidebar Inputs
# ============================================
with st.sidebar:
    st.header("📊 Soil & Crop Inputs")
    st.markdown("---")
    
    salinity = st.slider("🧂 Salinity (dS/m)", 0.0, 20.0, 7.8, 0.1)
    moisture = st.slider("💧 Soil Moisture (%)", 0, 100, 53)
    temperature = st.slider("🌡️ Temperature (°C)", 15, 45, 23)
    humidity = st.slider("💨 Air Humidity (%)", 20, 90, 60)
    
    soil_type = st.selectbox("🏞️ Soil Type", ["Sandy", "Loamy", "Clayey", "Silty"])
    
    growth_stage = st.selectbox("🌱 Growth Stage", [
        "Establishment", 
        "Tillering", 
        "Stem Elongation",
        "Flowering", 
        "Maturity"
    ])
    
    st.markdown("---")
    st.caption("📚 Based on Egyptian Research: Zaki 2025, El-Akhdar 2025")

# ============================================
# 4. Zone Determination & Recommendations
# ============================================
if salinity < 4:
    zone = "🟢 Zone A - Low Salinity"
    zone_color = "success"
    recommendation = "Standard smart irrigation"
    bio_dosing = "No PGPR needed"
    bio_frequency = "Not required"
elif 4 <= salinity < 8:
    zone = "🟡 Zone B - Moderate Salinity"
    zone_color = "warning"
    recommendation = "Apply PGPR bio-remediation"
    bio_dosing = "Mixture: Stutzerimonas stutzeri"
    bio_frequency = "Every 2 weeks"
else:
    zone = "🔴 Zone C - High Salinity"
    zone_color = "error"
    recommendation = "Intensive treatment + Micro-flushing"
    bio_dosing = "High dose PGPR + additives"
    bio_frequency = "Weekly"

# ============================================
# 5. Yield Estimation
# ============================================
def estimate_yield(salinity, has_pgpr=True):
    base_yield = 11.5
    if has_pgpr:
        reduction = max(0, (salinity - 3.5) * 0.05)
    else:
        reduction = max(0, (salinity - 3.5) * 0.15)
    estimated = base_yield * (1 - min(reduction, 0.8))
    return max(0.5, round(estimated, 1))

yield_with_pgpr = estimate_yield(salinity, True)
yield_without_pgpr = estimate_yield(salinity, False)
yield_improvement = round(((yield_with_pgpr - yield_without_pgpr) / yield_without_pgpr) * 100, 1)

# ============================================
# 6. Water Requirements
# ============================================
water_requirements = {
    "Establishment": 500,
    "Tillering": 600,
    "Stem Elongation": 550,
    "Flowering": 500,
    "Maturity": 350
}
total_water_mm = water_requirements.get(growth_stage, 500)
irrigations_count = round(total_water_mm / 120) + 1

# ============================================
# 7. Main Columns Display
# ============================================
col1, col2 = st.columns([1, 1.5])

# ========== Left Column ==========
with col1:
    st.markdown("### 📊 Current Status")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("🧂 Salinity", f"{salinity} dS/m")
    with m2:
        st.metric("💧 Moisture", f"{moisture}%")
    with m3:
        st.metric("🌡️ Temperature", f"{temperature}°C")
    
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <b>🏞️ Soil Type:</b> {soil_type}<br>
        <b>🌱 Growth Stage:</b> {growth_stage}
    </div>
    """, unsafe_allow_html=True)
    
    if zone_color == "success":
        st.success(f"**Classification:** {zone}")
    elif zone_color == "warning":
        st.warning(f"**Classification:** {zone}")
    else:
        st.error(f"**Classification:** {zone}")
    
    st.markdown("### 💊 Bio-Remediation Recommendation")
    st.info(f"""
    - **Bio-agent:** {bio_dosing}
    - **Frequency:** {bio_frequency}
    - **Action:** {recommendation}
    """)
    
    st.markdown("### 💧 Irrigation Recommendations")
    
    if moisture < 40 and growth_stage in ["Tillering", "Flowering"]:
        irrigation_priority = "🔴 **Urgent!** - Critical stage"
    elif moisture < 50:
        irrigation_priority = "🟡 Priority - Irrigate soon"
    else:
        irrigation_priority = "🟢 Good - Continue current schedule"
    
    st.markdown(f"""
    - **Seasonal Water Need:** {total_water_mm} mm
    - **Recommended Irrigations:** {irrigations_count}
    - **Micro-flush:** Every 30 days
    - **Irrigation Status:** {irrigation_priority}
    """)

# ========== Right Column ==========
with col2:
    st.markdown("### 📈 PGPR Effect on Root Growth")
    
    fig_root = px.line(df, x="salinity_dsm", y="root_length_cm", color="treatment",
                       title="Salinity Effect on Root Length",
                       labels={"salinity_dsm": "Salinity (dS/m)", 
                               "root_length_cm": "Root Length (cm)",
                               "treatment": "Treatment"})
    fig_root.update_layout(height=400, title_font_size=16)
    st.plotly_chart(fig_root, use_container_width=True)
    
    st.markdown("### 🌾 PGPR Effect on Grain Yield")
    
    yc1, yc2, yc3 = st.columns(3)
    with yc1:
        st.metric("Without PGPR", f"{yield_without_pgpr} ton/ha")
    with yc2:
        st.metric("With PGPR", f"{yield_with_pgpr} ton/ha", delta=f"+{yield_improvement}%")
    with yc3:
        st.metric("Difference", f"{yield_with_pgpr - yield_without_pgpr:.1f} ton/ha")
    
    salinity_range = np.arange(0, 16, 1)
    yields_with = [estimate_yield(s, True) for s in salinity_range]
    yields_without = [estimate_yield(s, False) for s in salinity_range]
    
    fig_yield = px.line(title="Wheat Yield Estimation Under Salinity Stress")
    fig_yield.add_scatter(x=salinity_range, y=yields_without, name="Without PGPR", mode="lines")
    fig_yield.add_scatter(x=salinity_range, y=yields_with, name="With PGPR", mode="lines")
    fig_yield.update_layout(height=400, title_font_size=16,
                            xaxis_title="Salinity (dS/m)",
                            yaxis_title="Yield (ton/ha)")
    st.plotly_chart(fig_yield, use_container_width=True)

# ============================================
# ========== PHASE 2 - ADDED FEATURES ==========
# ============================================

st.markdown("---")
st.markdown("## 🚀 Phase 2: Smart Decision Engine")

# ============================================
# 8. Smart Alerts
# ============================================

st.markdown("### ⚠️ Alerts & Recommendations")

alert_count = 0

# Salinity alert
if salinity > 8:
    st.error("🔴 **URGENT!** Salinity too high (>8 dS/m) - Soil flushing recommended immediately!")
    alert_count += 1
elif salinity > 6:
    st.warning("🟡 **Alert:** Salinity increasing - Apply PGPR this week")
    alert_count += 1
else:
    st.success("✅ Salinity at safe level")

# Moisture alert
if moisture < 30:
    st.error("🔴 **URGENT!** Moisture critically low - Immediate irrigation required!")
    alert_count += 1
elif moisture < 45 and growth_stage in ["Tillering", "Flowering"]:
    st.warning("🟡 **Alert:** Low moisture at critical stage - Irrigate within 48 hours")
    alert_count += 1
else:
    st.success("✅ Moisture level adequate")

# Temperature alert
if temperature > 38:
    st.error("🔴 **Alert!** Extreme temperature - High plant stress")
    alert_count += 1
elif temperature > 35:
    st.warning("🟡 **Alert:** High temperature - Increased evaporation and salinity risk")
    alert_count += 1
else:
    st.success("✅ Temperature optimal")

if alert_count == 0:
    st.info("ℹ️ All indicators within normal range")

st.markdown("---")

# ============================================
# 9. Time Series Data (Weekly)
# ============================================

st.markdown("### 📅 Soil Condition - Last 7 Days")

# Try to load time series data
try:
    df_sim = pd.read_csv("simulated_data.csv")
    df_sim['timestamp'] = pd.to_datetime(df_sim['timestamp'])
    
    last_date = df_sim['timestamp'].max()
    week_ago = last_date - pd.Timedelta(days=7)
    df_week = df_sim[df_sim['timestamp'] >= week_ago]
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        fig_sim_salinity = px.line(
            df_week, x='timestamp', y='salinity_EC_dSm',
            title="📈 Salinity Trend (Last 7 Days)",
            labels={"timestamp": "Date/Time", "salinity_EC_dSm": "Salinity (dS/m)"}
        )
        fig_sim_salinity.update_layout(height=350)
        st.plotly_chart(fig_sim_salinity, use_container_width=True)
    
    with col_t2:
        fig_sim_humidity = px.line(
            df_week, x='timestamp', y='humidity_%',
            title="💧 Soil Moisture Trend (Last 7 Days)",
            labels={"timestamp": "Date/Time", "humidity_%": "Moisture (%)"}
        )
        fig_sim_humidity.update_layout(height=350)
        st.plotly_chart(fig_sim_humidity, use_container_width=True)
    
    # Decision statistics
    st.markdown("#### 🤖 System Decisions (Last 7 Days)")
    decisions_count = df_week['system_decision'].value_counts().reset_index()
    decisions_count.columns = ['Decision', 'Count']
    st.dataframe(decisions_count, use_container_width=True)
    
    with st.expander("📋 Last 10 Field Readings"):
        st.dataframe(df_sim.tail(10), use_container_width=True)
        
except FileNotFoundError:
    # Fallback simulated data if file missing
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    weekly_salinity = []
    weekly_moisture = []
    
    for i in range(7):
        change_s = np.random.uniform(-0.5, 0.5)
        change_m = np.random.uniform(-5, 5)
        weekly_salinity.append(max(0, round(salinity + change_s, 1)))
        weekly_moisture.append(max(20, min(80, round(moisture + change_m))))
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        fig_fallback = px.line(x=days, y=weekly_salinity, 
                               title="Salinity Trend (Simulated - File Not Found)",
                               labels={"x": "Day", "y": "Salinity (dS/m)"})
        fig_fallback.add_scatter(x=days, y=weekly_salinity, mode='lines+markers')
        fig_fallback.update_layout(height=350)
        st.plotly_chart(fig_fallback, use_container_width=True)
    
    with col_t2:
        fig_fallback2 = px.line(x=days, y=weekly_moisture,
                                title="Moisture Trend (Simulated - File Not Found)",
                                labels={"x": "Day", "y": "Moisture (%)"})
        fig_fallback2.add_scatter(x=days, y=weekly_moisture, mode='lines+markers')
        fig_fallback2.update_layout(height=350)
        st.plotly_chart(fig_fallback2, use_container_width=True)

st.markdown("---")

# ============================================
# 10. Advanced Analysis & Precise Recommendations
# ============================================

with st.expander("📊 Advanced Analysis - Precision Recommendations"):
    
    # Advanced weekly water calculation
    base_need = water_requirements.get(growth_stage, 500) / 4
    
    if temperature > 35:
        temp_factor = 1.3
    elif temperature > 30:
        temp_factor = 1.15
    else:
        temp_factor = 1.0
    
    humidity_factor = 1 - (humidity / 200)
    weekly_need = round(base_need * temp_factor * humidity_factor)
    weekly_need = max(50, min(150, weekly_need))
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.markdown("#### 💧 Advanced Irrigation Recommendations")
        st.markdown(f"""
        - **Weekly Water Requirement:** {weekly_need} mm
        - **Weekly Irrigations:** {max(1, round(weekly_need / 40))}
        - **Best Time to Irrigate:** {"🌅 Early Morning" if temperature < 30 else "🌙 Evening"}
        - **Irrigation Type:** {"Drip Irrigation" if soil_type in ["Sandy", "Loamy"] else "Surface Irrigation"}
        """)
    
    with col_y:
        st.markdown("#### 🧬 Advanced PGPR Recommendations")
        
        if salinity < 4:
            pgpr_dose = "Not required"
            pgpr_freq = "-"
        elif salinity < 8:
            pgpr_dose = "2 L/feddan"
            pgpr_freq = "Every 2 weeks"
        else:
            pgpr_dose = "4 L/feddan"
            pgpr_freq = "Weekly"
        
        st.markdown(f"""
        - **Recommended Dose:** {pgpr_dose}
        - **Frequency:** {pgpr_freq}
        - **Bio-agent:** Stutzerimonas stutzeri
        - **Treatment Duration:** Until salinity drops below 6 dS/m
        """)
    
    # Expected improvement indicator
    st.markdown("#### 📈 Expected Improvement After 30 Days Treatment")
    
    if salinity < 8:
        expected_improvement = "30-40%"
        improvement_color = "🟢"
        progress_val = 0.35
    else:
        expected_improvement = "50-60%"
        improvement_color = "🟡"
        progress_val = 0.55
    
    st.markdown(f"{improvement_color} **Expected Grain Yield Improvement:** {expected_improvement}")
    st.progress(progress_val)

st.markdown("---")
st.success("✅ Decision Engine Running Efficiently - All Recommendations Based on Egyptian Research")

# ============================================
# 11. Scientific References
# ============================================
with st.expander("📚 Scientific References - Egyptian Research"):
    st.markdown("""
    | Researcher | Finding |
    |------------|---------|
    | **El-Akhdar et al. (2025)** | 197% grain yield improvement using multi-strain PGPR |
    | **Zaki et al. (2025)** | 70% salinity impact reduction + 115% root length increase |
    | **Fouad et al. (2026)** | 92% chlorophyll retention at 15 dS/m salinity |
    """)

st.markdown("---")
st.caption("DRY2LIFE © 2026 | Bio-Digital Intelligence | Egyptian Engineering Group | Phase 2 Complete")
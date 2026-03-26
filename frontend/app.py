import streamlit as st
import requests
import time
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Manufacturing Predictor", layout="wide", page_icon="🏭")

# ====================== ATTRACTIVE THEME ======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600&display=swap');

    body, .main {
        background: linear-gradient(135deg, #f8f1e9 0%, #e8d9c2 100%);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', sans-serif;
        color: #6b4426;
    }

    .stButton>button {
        background: linear-gradient(90deg, #9c6644, #b07a55);
        color: white;
        border-radius: 16px;
        padding: 14px 28px;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(156, 102, 68, 0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 10px 25px rgba(156, 102, 68, 0.4);
    }

    /* Warm sliders */
    .stSlider > div > div > div { background-color: #d4b99f !important; }
    .stSlider > div > div > div > div { background: linear-gradient(90deg, #9c6644, #c89a6e) !important; }

    .result-card {
        background: linear-gradient(145deg, #f5e8d3, #e8d4b8);
        padding: 40px 30px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(63, 42, 30, 0.15);
        border: 1px solid #e0c9a8;
    }

    .big-text {
        font-size: 54px;
        font-weight: 700;
        background: linear-gradient(90deg, #6b4426, #9c6644);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🏭 Manufacturing Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6b4426; font-size:18px;'>AI-Powered Output Prediction</p>", unsafe_allow_html=True)
st.divider()

left, right = st.columns([2.2, 1])

# ====================== INPUTS (LEFT) ======================
with left:
    st.markdown("### ⚙️ Machine Parameters")
    col1, col2 = st.columns(2)
    with col1:
        Injection_Temperature = st.slider("Injection Temperature (°C)", 100, 300, 200, key="inj_temp")
        Injection_Pressure    = st.slider("Injection Pressure (bar)", 10, 100, 50, key="inj_press")
        Cycle_Time            = st.slider("Cycle Time (s)", 10, 60, 30, key="cycle_time")
        Cooling_Time          = st.slider("Cooling Time (s)", 5, 30, 15, key="cool_time")

    with col2:
        Material_Viscosity    = st.slider("Material Viscosity", 50, 200, 120, key="visc")
        Ambient_Temperature   = st.slider("Ambient Temperature (°C)", 10, 50, 25, key="amb_temp")
        Machine_Age           = st.slider("Machine Age (years)", 1, 20, 5, key="age")
        Operator_Experience   = st.slider("Operator Experience (years)", 1, 10, 3, key="op_exp")

    st.markdown("### 📊 Performance Metrics")
    col3, col4 = st.columns(2)
    with col3:
        Maintenance_Hours        = st.slider("Maintenance Hours", 0, 200, 100, key="maint")
        Temperature_Pressure_Ratio = st.slider("Temp-Pressure Ratio", 1, 10, 4, key="tp_ratio")
        Total_Cycle_Time         = st.slider("Total Cycle Time (s)", 20, 100, 45, key="total_cycle")

    with col4:
        Efficiency_Score   = st.slider("Efficiency Score", 0.0, 1.0, 0.8, step=0.01, key="eff_score")
        Machine_Utilization = st.slider("Machine Utilization", 0.0, 1.0, 0.75, step=0.01, key="util")

    st.markdown("### 🔘 Operational Settings")
    c1, c2 = st.columns(2)
    with c1:
        shift_evening = st.toggle("🌅 Evening Shift", key="eve_shift")
        shift_night   = st.toggle("🌙 Night Shift", key="night_shift")
    with c2:
        machine_type = st.selectbox("Machine Type", ["Type_A", "Type_B", "Type_C"], key="mach_type")
        material     = st.selectbox("Material Grade", ["Economy", "Standard", "Premium"], key="mat_grade")

    day = st.selectbox("Day of Week", 
                       ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"], 
                       key="day")

# ====================== RIGHT PANEL ======================
with right:
    st.markdown("### 📈 Prediction Result")

    result_placeholder = st.empty()

    # Show initial or updated prediction
    if "prediction" not in st.session_state:
        result_placeholder.markdown("""
            <div class="result-card">
                <p style="color:#8c6f4f; font-size:18px;">Click Predict to see result</p>
                <div style="font-size:80px; margin:30px 0; opacity:0.3;">🏭</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        result_placeholder.markdown(f"""
            <div class="result-card">
                <p style="font-size:18px; color:#6b4426;">Predicted Output</p>
                <div class="big-text">{st.session_state['prediction']:.1f}</div>
                <p style="color:#8c6f4f; font-size:20px;">Parts per Hour</p>
            </div>
        """, unsafe_allow_html=True)

    predict_clicked = st.button("🚀 Predict Output", use_container_width=True, key="predict_btn")

    # ====================== ENCODING ======================
    Shift_Evening = 1 if shift_evening else 0
    Shift_Night = 1 if shift_night else 0

    Machine_Type_Type_B = 1 if machine_type == "Type_B" else 0
    Machine_Type_Type_C = 1 if machine_type == "Type_C" else 0

    Material_Grade_Premium = 1 if material == "Premium" else 0
    Material_Grade_Standard = 1 if material == "Standard" else 0

    dow_map = {
        "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
        "Thursday": "Thursday", "Saturday": "Saturday", "Sunday": "Sunday"
    }
    Day_of_Week_Monday = 1 if day == "Monday" else 0
    Day_of_Week_Tuesday = 1 if day == "Tuesday" else 0
    Day_of_Week_Wednesday = 1 if day == "Wednesday" else 0
    Day_of_Week_Thursday = 1 if day == "Thursday" else 0
    Day_of_Week_Saturday = 1 if day == "Saturday" else 0
    Day_of_Week_Sunday = 1 if day == "Sunday" else 0

    # ====================== LIVE CHART ======================
    if "prediction" in st.session_state:
        st.markdown("### 📊 Output vs Efficiency Score")

        efficiency_values = [i/10 for i in range(1, 11)]
        predictions = []

        for eff in efficiency_values:
            temp_input = {
                "Injection_Temperature": Injection_Temperature,
                "Injection_Pressure": Injection_Pressure,
                "Cycle_Time": Cycle_Time,
                "Cooling_Time": Cooling_Time,
                "Material_Viscosity": Material_Viscosity,
                "Ambient_Temperature": Ambient_Temperature,
                "Machine_Age": Machine_Age,
                "Operator_Experience": Operator_Experience,
                "Maintenance_Hours": Maintenance_Hours,
                "Temperature_Pressure_Ratio": Temperature_Pressure_Ratio,
                "Total_Cycle_Time": Total_Cycle_Time,
                "Efficiency_Score": eff,
                "Machine_Utilization": Machine_Utilization,
                "Shift_Evening": Shift_Evening,
                "Shift_Night": Shift_Night,
                "Machine_Type_Type_B": Machine_Type_Type_B,
                "Machine_Type_Type_C": Machine_Type_Type_C,
                "Material_Grade_Premium": Material_Grade_Premium,
                "Material_Grade_Standard": Material_Grade_Standard,
                "Day_of_Week_Monday": Day_of_Week_Monday,
                "Day_of_Week_Tuesday": Day_of_Week_Tuesday,
                "Day_of_Week_Wednesday": Day_of_Week_Wednesday,
                "Day_of_Week_Thursday": Day_of_Week_Thursday,
                "Day_of_Week_Saturday": Day_of_Week_Saturday,
                "Day_of_Week_Sunday": Day_of_Week_Sunday,
            }

            try:
                backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
                response = requests.post(f"{backend_url}/predict", json=temp_input, timeout=5)
                pred = response.json()["prediction"]
                predictions.append(pred)
            except:
                predictions.append(0)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=efficiency_values, y=predictions,
                                 mode='lines+markers',
                                 line=dict(color='#9c6644', width=4),
                                 marker=dict(size=8, color='#c89a6e')))

        fig.update_layout(title="Sensitivity to Efficiency Score",
                          xaxis_title="Efficiency Score",
                          yaxis_title="Predicted Parts/Hour",
                          template="plotly_white", height=340)

        st.plotly_chart(fig, use_container_width=True)

# ====================== PREDICTION ON BUTTON CLICK ======================
# ====================== PREDICTION ON BUTTON CLICK ======================
if predict_clicked:
    with st.spinner("Predicting... ⏳"):
        time.sleep(0.8)

        input_data = {
            "Injection_Temperature": Injection_Temperature,
            "Injection_Pressure": Injection_Pressure,
            "Cycle_Time": Cycle_Time,
            "Cooling_Time": Cooling_Time,
            "Material_Viscosity": Material_Viscosity,
            "Ambient_Temperature": Ambient_Temperature,
            "Machine_Age": Machine_Age,
            "Operator_Experience": Operator_Experience,
            "Maintenance_Hours": Maintenance_Hours,
            "Temperature_Pressure_Ratio": Temperature_Pressure_Ratio,
            "Total_Cycle_Time": Total_Cycle_Time,
            "Efficiency_Score": Efficiency_Score,
            "Machine_Utilization": Machine_Utilization,
            "Shift_Evening": Shift_Evening,
            "Shift_Night": Shift_Night,
            "Machine_Type_Type_B": Machine_Type_Type_B,
            "Machine_Type_Type_C": Machine_Type_Type_C,
            "Material_Grade_Premium": Material_Grade_Premium,
            "Material_Grade_Standard": Material_Grade_Standard,
            "Day_of_Week_Monday": Day_of_Week_Monday,
            "Day_of_Week_Tuesday": Day_of_Week_Tuesday,
            "Day_of_Week_Wednesday": Day_of_Week_Wednesday,
            "Day_of_Week_Thursday": Day_of_Week_Thursday,
            "Day_of_Week_Saturday": Day_of_Week_Saturday,
            "Day_of_Week_Sunday": Day_of_Week_Sunday,
        }

        try:
            # ✅ Use environment variable for Docker compatibility
            backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
            response = requests.post(f"{backend_url}/predict", json=input_data, timeout=8)
            
            result = response.json()
            st.session_state["prediction"] = result["prediction"]
            st.rerun()

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
import streamlit as st
import requests
import time
import plotly.graph_objects as go


st.set_page_config(page_title="Manufacturing Predictor", layout="wide")

# --------------------------
# 🎨 Custom Beige-Brown Theme
# --------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f5ebe0, #e6ccb2);
    }
    .main {
        background: linear-gradient(135deg, #f5ebe0, #e6ccb2);
    }

    h1, h2, h3 {
        color: #5e3023;
    }

    .stButton>button {
        background-color: #7f5539;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 18px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #9c6644;
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }

    .result-card {
        background: linear-gradient(145deg, #ede0d4, #e6ccb2);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 4px 4px 20px rgba(0,0,0,0.1);
    }

    .big-text {
        font-size: 42px;
        color: #6f1d1b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# --------------------------
# Title
# --------------------------
st.title("🏭 Manufacturing Output Prediction")
st.markdown("Optimize your machine performance with AI 🚀")

st.divider()

# --------------------------
# Layout
# --------------------------
left, right = st.columns([2, 1])

# --------------------------
# LEFT SIDE INPUTS
# --------------------------
with left:
    st.subheader("⚙️ Machine Parameters")

    col1, col2 = st.columns(2)

    with col1:
        Injection_Temperature = st.slider("Injection Temperature", 100, 300, 200)
        Injection_Pressure = st.slider("Injection Pressure", 10, 100, 50)
        Cycle_Time = st.slider("Cycle Time", 10, 60, 30)
        Cooling_Time = st.slider("Cooling Time", 5, 30, 15)

    with col2:
        Material_Viscosity = st.slider("Material Viscosity", 50, 200, 120)
        Ambient_Temperature = st.slider("Ambient Temperature", 10, 50, 25)
        Machine_Age = st.slider("Machine Age", 1, 20, 5)
        Operator_Experience = st.slider("Operator Experience", 1, 10, 3)

    st.subheader("📊 Performance Metrics")

    col3, col4 = st.columns(2)

    with col3:
        Maintenance_Hours = st.slider("Maintenance Hours", 0, 200, 100)
        Temperature_Pressure_Ratio = st.slider("Temp-Pressure Ratio", 1, 10, 4)
        Total_Cycle_Time = st.slider("Total Cycle Time", 20, 100, 45)

    with col4:
        Efficiency_Score = st.slider("Efficiency Score", 0.0, 1.0, 0.8)
        Machine_Utilization = st.slider("Machine Utilization", 0.0, 1.0, 0.75)

    st.subheader("🔘 Categorical Inputs")

    shift_evening = st.toggle("Evening Shift")
    shift_night = st.toggle("Night Shift")

    machine_type = st.selectbox("Machine Type", ["Type_A", "Type_B", "Type_C"])
    material = st.selectbox("Material Grade", ["Economy", "Standard", "Premium"])
    day = st.selectbox("Day of Week", 
                       ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"])

# --------------------------
# RIGHT SIDE RESULT CARD
# --------------------------
with right:
    st.subheader("📈 Prediction Result")

    result_placeholder = st.empty()

    if "prediction" not in st.session_state:
        result_placeholder.markdown("""
            <div class="result-card">
                <p>Click Predict to see result</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        result_placeholder.markdown(f"""
            <div class="result-card">
                <p>Predicted Output</p>
                <div class="big-text">{st.session_state['prediction']:.2f}</div>
                <p>Parts / Hour</p>
            </div>
        """, unsafe_allow_html=True)

    

    st.markdown("<br>", unsafe_allow_html=True)

    # 🚀 BUTTON MOVED HERE
    predict_clicked = st.button("🚀 Predict Output")
# --------------------------
# Encoding
# --------------------------
    Shift_Evening = 1 if shift_evening else 0
    Shift_Night = 1 if shift_night else 0

    Machine_Type_Type_B = 1 if machine_type == "Type_B" else 0
    Machine_Type_Type_C = 1 if machine_type == "Type_C" else 0

    Material_Grade_Premium = 1 if material == "Premium" else 0
    Material_Grade_Standard = 1 if material == "Standard" else 0

    Day_of_Week_Monday = 1 if day == "Monday" else 0
    Day_of_Week_Saturday = 1 if day == "Saturday" else 0
    Day_of_Week_Sunday = 1 if day == "Sunday" else 0
    Day_of_Week_Thursday = 1 if day == "Thursday" else 0
    Day_of_Week_Tuesday = 1 if day == "Tuesday" else 0
    Day_of_Week_Wednesday = 1 if day == "Wednesday" else 0

# --------------------------
# 📊 Live Chart
# --------------------------
    if "prediction" in st.session_state:

        # Generate efficiency range
        efficiency_values = [i/10 for i in range(1, 11)]  # 0.1 → 1.0
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
                "Efficiency_Score": eff,  # ✅ FIXED
                "Machine_Utilization": Machine_Utilization,
                "Shift_Evening": Shift_Evening,
                "Shift_Night": Shift_Night,
                "Machine_Type_Type_B": Machine_Type_Type_B,
                "Machine_Type_Type_C": Machine_Type_Type_C,
                "Material_Grade_Premium": Material_Grade_Premium,
                "Material_Grade_Standard": Material_Grade_Standard,
                "Day_of_Week_Monday": Day_of_Week_Monday,
                "Day_of_Week_Saturday": Day_of_Week_Saturday,
                "Day_of_Week_Sunday": Day_of_Week_Sunday,
                "Day_of_Week_Thursday": Day_of_Week_Thursday,
                "Day_of_Week_Tuesday": Day_of_Week_Tuesday,
                "Day_of_Week_Wednesday": Day_of_Week_Wednesday
            }
        

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=temp_input
                )
                pred = response.json()["prediction"]
                predictions.append(pred)
            except:
                predictions.append(None)

        # Create chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=efficiency_values,
            y=predictions,
            mode='lines+markers',
            name='Prediction',
            line=dict(width=3)
        ))

        fig.update_layout(
            title="📊 Output vs Efficiency",
            xaxis_title="Efficiency Score",
            yaxis_title="Predicted Output",
            template="plotly_dark",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Predict Button
# --------------------------
st.divider()

if predict_clicked:


    with st.spinner("Predicting... ⏳"):
        time.sleep(1)  # smooth UX

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
            "Day_of_Week_Saturday": Day_of_Week_Saturday,
            "Day_of_Week_Sunday": Day_of_Week_Sunday,
            "Day_of_Week_Thursday": Day_of_Week_Thursday,
            "Day_of_Week_Tuesday": Day_of_Week_Tuesday,
            "Day_of_Week_Wednesday": Day_of_Week_Wednesday
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=input_data
            )

            result = response.json()
            st.session_state["prediction"] = result["prediction"]

            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import pandas as pd
from inference import detect_anomaly, detect_anomaly_and_carbon

st.title("Room Energy Digital Twin")

uploaded_file = st.file_uploader("Upload room data (CSV)")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if len(df) >= 30:
        error, is_anomaly = detect_anomaly(df.tail(30))

        st.metric("Reconstruction Error", round(error, 5))

        if is_anomaly:
            st.error("Anomaly Detected ⚠️")
        else:
            st.success("Normal Operation ✅")
error, is_anomaly, energy, carbon = detect_anomaly_and_carbon(df.tail(30))

st.metric("Energy Used (kWh)", round(energy, 2))
st.metric("Carbon Emission (kg CO₂)", round(carbon, 2))
    
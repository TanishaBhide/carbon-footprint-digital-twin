import numpy as np
import joblib
from tensorflow.keras.models import load_model # type: ignore
from carbon import calculate_carbon

def detect_anomaly_and_carbon(df_window):
    error, is_anomaly = detect_anomaly(df_window)

    total_energy = df_window["energy_kWh"].sum()
    carbon_emission = calculate_carbon(total_energy)

    return error, is_anomaly, total_energy, carbon_emission

WINDOW_SIZE = 30

SENSOR_COLS = [
    "occupancy",
    "temperature_C",
    "AC",
    "Fan",
    "Light",
    "energy_kWh",
    "is_holiday"
]

model = load_model("model/lstm_autoencoder.h5")
scaler = joblib.load("model/scaler.save")

THRESHOLD = 0.015  # replace with printed value if you stored it

def detect_anomaly(df_window):
    data = df_window[SENSOR_COLS].values
    data = scaler.transform(data)
    data = data.reshape(1, WINDOW_SIZE, len(SENSOR_COLS))

    recon = model.predict(data)
    error = np.mean(np.square(data - recon))

    return error, error > THRESHOLD

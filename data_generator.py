import numpy as np
import pandas as pd
from datetime import datetime

# -----------------------
# Configurations
# -----------------------
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
NUM_ROOMS = 30

# Generate timestamps for each hour in the year
timestamps = pd.date_range(start=START_DATE, end=END_DATE, freq="h")

# Room IDs
rooms = [f"Room_{i+1}" for i in range(NUM_ROOMS)]

# Festival holidays (India-oriented)
FESTIVAL_HOLIDAYS = pd.to_datetime([
    "2024-01-14",  # Pongal
    "2024-01-26",  # Republic Day
    "2024-04-09",  # Ugadi
    "2024-08-15",  # Independence Day
    "2024-10-02",  # Gandhi Jayanti
    "2024-10-31",  # Diwali
    "2024-11-01",  # Karnataka Rajyotsava
    "2024-12-25",  # Christmas
])

# -----------------------
# Helper Functions
# -----------------------
def is_holiday(ts):
    """
    Returns True if the timestamp falls under any holiday condition
    """
    # Entire September holiday
    if ts.month == 9:
        return True

    # 8-day March holiday (March 10–17)
    if ts.month == 3 and 10 <= ts.day <= 17:
        return True

    # Festival holidays
    if ts.normalize() in FESTIVAL_HOLIDAYS:
        return True

    return False

def went_home_on_weekend():
    """
    35% chance that students leave hostel for weekend
    """
    return np.random.choice([0, 1], p=[0.65, 0.35])

def get_occupancy(hour, day_of_week, weekend_empty, holiday):
    """
    Returns number of occupants in a room (0–3)
    Holiday → mostly occupied (~70%)
    """
    # HOLIDAY LOGIC
    if holiday:
        return np.random.choice(
            [0, 1, 2, 3],
            p=[0.3, 0.25, 0.3, 0.15]
        )

    # WEEKEND LOGIC
    if day_of_week >= 5:
        if weekend_empty:
            return 0
        if 10 <= hour <= 22:
            return np.random.choice([1, 2, 3], p=[0.3, 0.45, 0.25])
        else:
            return np.random.choice([1, 2], p=[0.6, 0.4])

    # WEEKDAY LOGIC
    if 9 <= hour <= 17:
        return np.random.choice([0, 1], p=[0.75, 0.25])
    else:
        return np.random.choice([1, 2, 3], p=[0.45, 0.4, 0.15])

def get_temperature(month, hour):
    """
    Bangalore-like temperature simulation with day-night variation
    """
    seasonal_base = {
        1: 20, 2: 22, 3: 25, 4: 27,
        5: 28, 6: 25, 7: 24, 8: 24,
        9: 23, 10: 23, 11: 22, 12: 21
    }
    base_temp = seasonal_base[month]

    # Day-night fluctuation
    if 6 <= hour <= 18:
        temp = base_temp + np.random.normal(2, 1)
    else:
        temp = base_temp + np.random.normal(-1, 1)

    return round(temp, 1)

def device_states(occupancy, hour, temperature):
    """
    Determines ON/OFF states of AC, Fan, Lights
    """
    Light = 1 if occupancy > 0 and (hour < 6 or hour > 18) else 0
    Fan = 1 if occupancy > 0 and temperature >= 22 else 0
    AC = 1 if occupancy > 0 and temperature >= 28 else 0
    return AC, Fan, Light

def energy_usage(AC, Fan, Light):
    """
    Returns energy consumption (kWh) per hour
    Includes small noise to avoid overfitting
    """
    energy = AC * 1.5 + Fan * 0.75 + Light * 0.2
    noise = np.random.normal(0, 0.05)
    return round(max(energy + noise, 0), 3)

# -----------------------
# Data Generation
# -----------------------
data = []

for room in rooms:
    weekend_empty_flag = {}
    for ts in timestamps:
        hour = ts.hour
        day_of_week = ts.dayofweek
        week = ts.isocalendar().week

        holiday = is_holiday(ts)

        # Decide once per weekend if students leave
        if day_of_week >= 5 and week not in weekend_empty_flag:
            weekend_empty_flag[week] = went_home_on_weekend()

        weekend_empty = weekend_empty_flag.get(week, 0)

        occupancy = get_occupancy(hour, day_of_week, weekend_empty, holiday)
        temperature = get_temperature(ts.month, hour)
        AC, Fan, Light = device_states(occupancy, hour, temperature)
        energy = energy_usage(AC, Fan, Light)

        data.append([
            ts, room, occupancy, temperature,
            AC, Fan, Light, energy, holiday
        ])

# Column names
columns = [
    "timestamp", "room_id", "occupancy",
    "temperature_C", "AC", "Fan", "Light",
    "energy_kWh", "is_holiday"
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save full dataset
df.to_csv("synthetic_hostel_energy_dataset.csv", index=False)
print("✅ Full dataset saved as 'synthetic_hostel_energy_dataset.csv'")

# Save a small sample head (5 rows) for GitHub
df.head(5).to_csv("synthetic_hostel_energy_dataset_sample.csv", index=False)
print("✅ Sample dataset saved as 'synthetic_hostel_energy_dataset_sample.csv'")

# Preview
print(df.head())

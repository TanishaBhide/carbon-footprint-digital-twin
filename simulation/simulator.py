import pandas as pd

from digital_twin.appliance_model import Appliance
from digital_twin.room_model import Room
from digital_twin.floor_model import Floor
from digital_twin.occupancy_rules import is_room_occupied

def create_hostel_floor():
    appliances = [
        Appliance("Light", 0.02),
        Appliance("Fan", 0.075),
        Appliance("AC", 1.5),
        Appliance("Plug Load", 0.1)
    ]

    rooms = [Room(f"Room_{i}", appliances) for i in range(101, 107)]
    return Floor(rooms)

def simulate_one_day(floor: Floor):
    records = []

    for hour in range(24):
        for room in floor.rooms:
            energy = room.energy_for_duration(1) if is_room_occupied(hour) else 0.0

            records.append({
                "room_id": room.room_id,
                "hour": hour,
                "energy_kwh": round(energy, 3)
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    floor = create_hostel_floor()
    df = simulate_one_day(floor)
    df.to_csv("data/processed/simulated_energy_day.csv", index=False)
    print("Digital twin simulation completed.")

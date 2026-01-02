EMISSION_FACTOR = 0.82  # kg CO2 per kWh

def calculate_carbon(energy_kWh):
    return energy_kWh * EMISSION_FACTOR

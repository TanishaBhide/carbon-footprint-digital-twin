class Room:
    """
    Represents a hostel room in the digital twin.
    """

    def __init__(self, room_id: str, appliances: list, occupancy: int = 2):
        self.room_id = room_id
        self.appliances = appliances
        self.occupancy = occupancy

    def energy_for_duration(self, hours: float) -> float:
        return sum(a.energy_consumption(hours) for a in self.appliances)

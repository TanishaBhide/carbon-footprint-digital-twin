class Floor:
    """
    Aggregates multiple rooms into a single hostel floor.
    """

    def __init__(self, rooms: list):
        self.rooms = rooms

    def total_energy(self, hours: float) -> float:
        return sum(room.energy_for_duration(hours) for room in self.rooms)

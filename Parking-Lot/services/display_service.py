from models.parking_lot import ParkingLot
from models.vechicles import Vehicle, VehicleType


class DisplayService:
    def __init__(self, parking_lot: ParkingLot):
        self.parking_lot = parking_lot

    def display_free_count(self, vehicle_type: VehicleType):
        for floor in self.parking_lot.floors:
            no_of_free_slot = floor.get_free_slots_count(vehicle_type)
            print(
                f"No. of free slots for {vehicle_type.value} on Floor {floor.floor_number}: {no_of_free_slot}"
            )

    def display_free_slots(self, vehicle_type: VehicleType):
        for floor in self.parking_lot.floors:
            free_slots = floor.get_free_slots(vehicle_type)
            slot_numbers = ", ".join(map(str, free_slots))
            print(
                f"Free slots for {vehicle_type.value} on Floor {floor.floor_number}: {slot_numbers or None}"
            )

    def display_occupied_slots(self, vehicle_type: VehicleType):
        for floor in self.parking_lot.floors:
            slots = floor.get_occupied_slots(vehicle_type)
            slot_numbers = ", ".join(map(str, slots))

            print(
                f"Occupied slots for {vehicle_type.value} "
                f"on Floor {floor.floor_number}: {slot_numbers or None}"
            )

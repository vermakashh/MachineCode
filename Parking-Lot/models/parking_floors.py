from dataclasses import dataclass, field
from typing import List, Optional
from models.vechicles import Vehicle, VehicleType
from models.parking_slots import ParkingSlot


@dataclass
class ParkingFloor:
    floor_number: int
    slots: List[ParkingSlot] = field(default_factory=list)

    def add_slots(self, number_of_slots: int):
        for slot_number in range(1, number_of_slots + 1):
            if slot_number == 1:
                vehcile_type = VehicleType.TRUCK
            elif slot_number in (2, 3):
                vehcile_type = VehicleType.BIKE
            else:
                vehcile_type = VehicleType.CAR

            self.slots.append(ParkingSlot(slot_number, vehcile_type))

    def find_available_slot(self, vehcile_type: VehicleType) -> Optional[ParkingSlot]:
        for slots in self.slots:
            if slots.vehicle_type == vehcile_type and slots.is_available():
                return slots

        return None

    def get_free_slots(self, vehicle_type: VehicleType) -> list[int]:
        return [
            slot.slot_number
            for slot in self.slots
            if slot.vehicle_type == vehicle_type and slot.is_available()
        ]

    def get_occupied_slots(self, vehicle_type: VehicleType) -> list[int]:
        return [
            slot.slot_number
            for slot in self.slots
            if slot.vehicle_type == vehicle_type and not slot.is_available()
        ]

    def get_free_slots_count(self, vehicle_type: VehicleType) -> int:
        return len(self.get_free_slots(vehicle_type))

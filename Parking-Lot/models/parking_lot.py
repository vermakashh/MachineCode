from dataclasses import dataclass, field
from typing import Optional

from models.vechicles import VehicleType
from models.parking_slots import ParkingSlot
from models.parking_floors import ParkingFloor


@dataclass
class ParkingLot:
    parking_lot_id: str
    floors: list[ParkingFloor] = field(default_factory=list)

    def add_floors(self, number_of_floors: int, number_of_slots: int):
        for floor_number in range(1, number_of_floors + 1):
            floor = ParkingFloor(floor_number)
            floor.add_slots(number_of_slots)

            self.floors.append(floor)

    def find_available_slot(
        self, vehicle_type: VehicleType
    ) -> Optional[tuple[ParkingFloor, ParkingSlot]]:
        for floor in self.floors:
            slot = floor.find_available_slot(vehicle_type)

            if slot is not None:
                return floor, slot

        return None

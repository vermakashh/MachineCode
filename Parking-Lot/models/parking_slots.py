from dataclasses import dataclass
from typing import Optional

from models.vechicles import Vehicle, VehicleType


@dataclass
class ParkingSlot:
    slot_number: int
    vehicle_type: VehicleType
    vehicle: Optional[Vehicle] = None

    def is_available(self) -> bool:
        return self.vehicle is None

    def can_park_vehicle(self, vehicle: Vehicle) -> bool:
        return self.is_available() and self.vehicle_type == vehicle.vehicle_type

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        if not self.can_park_vehicle(vehicle):
            return False

        self.vehicle = vehicle
        return True

    def unpark_vehicle(self) -> Optional[Vehicle]:
        if not self.is_available():
            vehicle = self.vehicle
            self.vehicle = None
            return vehicle

from dataclasses import dataclass
from enum import Enum


class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"


@dataclass
class Vehicle:
    vehicle_type: VehicleType
    registration_number: str
    color: str

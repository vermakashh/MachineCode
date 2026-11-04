from typing import Optional, Dict

from models.vechicles import Vehicle
from models.parking_lot import ParkingLot
from models.ticket import Ticket
from utils.ticket_generator import ticket_id_generator


class ParkingLotManager:

    def __init__(self):
        self.parking_lot: Optional[ParkingLot] = None
        self.active_tickets: Dict[str, Ticket] = {}

    def create_parking_lot(
        self, parking_lot_id: str, no_of_floors: int, no_of_slots_per_floor: int
    ):
        self.parking_lot = ParkingLot(parking_lot_id)
        self.parking_lot.add_floors(no_of_floors, no_of_slots_per_floor)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        if self.parking_lot is None:
            return None

        result = self.parking_lot.find_available_slot(vehicle.vehicle_type)

        if result is None:
            return None

        floor, slot = result

        if not slot.park_vehicle(vehicle):
            return None

        ticket_id = ticket_id_generator(
            self.parking_lot.parking_lot_id, floor.floor_number, slot.slot_number
        )

        ticket = Ticket(ticket_id, vehicle, floor.floor_number, slot.slot_number)

        self.active_tickets[ticket_id] = ticket

        return ticket

    def unpark_vehicle(self, ticket_id: str) -> Optional[Vehicle]:

        if self.parking_lot is None:
            return None

        ticket = self.active_tickets.get(ticket_id)

        if ticket is None:
            return None

        floor = self.parking_lot.floors[ticket.floor_number - 1]

        slot = floor.slots[ticket.slot_number - 1]

        vehicle = slot.unpark_vehicle()

        if vehicle is None:
            return None

        del self.active_tickets[ticket_id]

        return vehicle

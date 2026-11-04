from dataclasses import dataclass
from models.vechicles import Vehicle


@dataclass
class Ticket:
    ticket_id: str
    vehicle: Vehicle
    floor_number: int
    slot_number: int

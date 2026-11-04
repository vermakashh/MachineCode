def ticket_id_generator(
    parking_lot_id: str, floor_number: int, slot_number: int
) -> str:
    ticket = f"{parking_lot_id}_{floor_number}_{slot_number}"
    return ticket

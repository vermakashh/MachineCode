from models.vechicles import Vehicle, VehicleType
from services.parking_lot_manager import ParkingLotManager
from services.display_service import DisplayService


def main():
    manager = ParkingLotManager()
    display_service = None

    while True:
        command = input().strip()

        if not command:
            continue

        parts = command.split()
        action = parts[0]

        if action == "create_parking_lot":
            parking_lot_id = parts[1]
            no_of_floors = int(parts[2])
            slots_per_floor = int(parts[3])

            manager.create_parking_lot(parking_lot_id, no_of_floors, slots_per_floor)

            display_service = DisplayService(manager.parking_lot)

        elif action == "park_vehicle":
            vehicle_type = VehicleType(parts[1])
            registration_number = parts[2]
            color = parts[3]

            vehicle = Vehicle(
                vehicle_type=vehicle_type,
                registration_number=registration_number,
                color=color,
            )

            ticket = manager.park_vehicle(vehicle)

            if ticket is None:
                print("Parking Lot is full")
            else:
                print(f"Parked vehicle. Ticket ID: {ticket.ticket_id}")

        elif action == "unpark_vehicle":
            ticket_id = parts[1]
            vehicle = manager.unpark_vehicle(ticket_id)

            if vehicle is None:
                print("Invalid ticket")
            else:
                print(
                    f"Unparked vehicle with Registration Number: "
                    f"{vehicle.registration_number} and Color: {vehicle.color}"
                )

        elif action == "display":
            if display_service is None:
                print("Please create a parking lot first")
                continue

            display_type = parts[1]
            vehicle_type = VehicleType(parts[2])

            if display_type == "free_count":
                display_service.display_free_count(vehicle_type)

            elif display_type == "free_slots":
                display_service.display_free_slots(vehicle_type)

            elif display_type == "occupied_slots":
                display_service.display_occupied_slots(vehicle_type)

        elif action == "exit":
            break


if __name__ == "__main__":
    main()

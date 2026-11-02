import json

from services.project_manager import ProjectManager
from utils.serializer import (
    board_to_dict,
    list_to_dict,
    card_to_dict,
)


class CLI:
    def __init__(self, manager: ProjectManager):
        self.manager = manager

    def print_json(self, data):
        print(json.dumps(data, indent=2))

    def execute(self, command: str):
        command = command.strip()
        if not command:
            return

        try:
            self._execute(command)
        except ValueError as error:
            print(f"Error: {error}")

    def _execute(self, command: str):
        parts = command.split()

        if parts[0] == "SHOW":
            self._show(parts)
        elif parts[0] == "BOARD":
            self._board(command, parts)
        elif parts[0] == "LIST":
            self._list(command, parts)
        elif parts[0] == "CARD":
            self._card(command, parts)
        else:
            raise ValueError("Unknown command")

    def _show(self, parts):
        if len(parts) == 1:
            boards = self.manager.get_all_boards()
            if not boards:
                print("No boards")
                return
            self.print_json([board_to_dict(board) for board in boards])

        elif len(parts) == 3 and parts[1] == "BOARD":
            self.print_json(board_to_dict(self.manager.get_board(parts[2])))

        elif len(parts) == 3 and parts[1] == "LIST":
            self.print_json(list_to_dict(self.manager.get_list(parts[2])))

        elif len(parts) == 3 and parts[1] == "CARD":
            self.print_json(card_to_dict(self.manager.get_card(parts[2])))

        else:
            raise ValueError("Invalid SHOW command")

    def _board(self, command, parts):
        if len(parts) >= 3 and parts[1] == "CREATE":
            remainder = command.split("CREATE", 1)[1].strip()
            tokens = remainder.split()

            privacy = "PUBLIC"
            if tokens[-1].upper() in ("PUBLIC", "PRIVATE"):
                privacy = tokens.pop()

            name = " ".join(tokens)
            board = self.manager.create_board(name, privacy)
            print(f"Created board: {board.id}")
            return

        if len(parts) == 3 and parts[1] == "DELETE":
            self.manager.delete_board(parts[2])
            print(f"Deleted board: {parts[2]}")
            return

        if len(parts) >= 4:
            board_id = parts[1]
            operation = parts[2].upper()

            if operation in ("ADD_MEMBER", "REMOVE_MEMBER"):
                if len(parts) != 4:
                    raise ValueError("Expected a user ID")

                if operation == "ADD_MEMBER":
                    self.manager.add_member(board_id, parts[3])
                else:
                    self.manager.remove_member(board_id, parts[3])
                return

            attribute = parts[2].lower()
            value = command.split(None, 3)[3]
            self.manager.update_board(board_id, attribute, value)
            return

        raise ValueError("Invalid BOARD command")

    def _list(self, command, parts):
        if len(parts) >= 4 and parts[1] == "CREATE":
            board_id = parts[2]
            name = command.split(None, 3)[3]
            task_list = self.manager.create_list(board_id, name)
            print(f"Created list: {task_list.id}")
            return

        if len(parts) == 3 and parts[1] == "DELETE":
            self.manager.delete_list(parts[2])
            print(f"Deleted list: {parts[2]}")
            return

        if len(parts) >= 4:
            list_id = parts[1]
            attribute = parts[2].lower()
            value = command.split(None, 3)[3]
            self.manager.update_list(list_id, attribute, value)
            return

        raise ValueError("Invalid LIST command")

    def _card(self, command, parts):
        if len(parts) >= 4 and parts[1] == "CREATE":
            list_id = parts[2]
            name = command.split(None, 3)[3]
            card = self.manager.create_card(list_id, name)
            print(f"Created card: {card.id}")
            return

        if len(parts) == 3 and parts[1] == "DELETE":
            self.manager.delete_card(parts[2])
            print(f"Deleted card: {parts[2]}")
            return

        if len(parts) >= 3:
            card_id = parts[1]
            operation = parts[2].upper()

            if operation == "ASSIGN" and len(parts) == 4:
                self.manager.assign_card(card_id, parts[3])
                return

            if operation == "UNASSIGN" and len(parts) == 3:
                self.manager.unassign_card(card_id)
                return

            if operation == "MOVE" and len(parts) == 4:
                self.manager.move_card(card_id, parts[3])
                return

            if operation in ("NAME", "DESCRIPTION") and len(parts) >= 4:
                attribute = operation.lower()
                value = command.split(None, 3)[3]
                self.manager.update_card(card_id, attribute, value)
                return

        raise ValueError("Invalid CARD command")

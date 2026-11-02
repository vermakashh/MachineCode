from models.user import User
from models.board import Board, Privacy
from models.task_list import TaskList
from models.card import Card
from utils.id_generator import generate_id


class ProjectManager:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.boards: dict[str, Board] = {}

    def add_user(self, user: User) -> None:
        if user.user_id in self.users:
            raise ValueError(f"User with ID {user.user_id} already exists.")

        if any(existing.email == user.email for existing in self.users.values()):
            raise ValueError(f"User with email {user.email} already exists.")

        self.users[user.user_id] = user

    def get_user(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} does not exist.")
        return user

    def create_board(self, name: str, privacy: str = "PUBLIC") -> Board:
        if not name.strip():
            raise ValueError("Board name cannot be empty.")

        try:
            board_privacy = Privacy(privacy.upper())
        except ValueError:
            raise ValueError(
                f"Invalid privacy setting: {privacy}. Must be 'PUBLIC' or 'PRIVATE'."
            ) from None

        board_id = generate_id()

        board = Board(
            id=board_id,
            name=name,
            privacy=board_privacy,
            url=f"https://trello.com/boards/{board_id}",
        )

        self.boards[board_id] = board
        return board

    def get_board(self, board_id: str) -> Board:
        board = self.boards.get(board_id)
        if board is None:
            raise ValueError(f"Board with ID {board_id} does not exist.")
        return board

    def get_all_boards(self) -> list[Board]:
        return list(self.boards.values())

    def update_board(self, board_id: str, attribute: str, value: str) -> Board:
        board = self.get_board(board_id)

        if attribute == "name":
            if not value.strip():
                raise ValueError("Board name cannot be empty.")
            board.name = value
        elif attribute == "privacy":
            try:
                board.privacy = Privacy(value.upper())
            except ValueError:
                raise ValueError(
                    f"Invalid privacy setting: {value}. Must be 'PUBLIC' or 'PRIVATE'."
                ) from None
        else:
            raise ValueError(f"Invalid attribute: {attribute}.")

        return board

    def add_member(self, board_id: str, user_id: str) -> Board:
        board = self.get_board(board_id)
        user = self.get_user(user_id)

        if user_id in board.members:
            raise ValueError(
                f"User with ID {user_id} is already a member of the board."
            )

        board.members[user_id] = user
        return board

    def remove_member(self, board_id: str, user_id: str) -> Board:
        board = self.get_board(board_id)
        user = self.get_user(user_id)

        if user_id not in board.members:
            raise ValueError(f"User with ID {user_id} is not a member of the board.")

        del board.members[user_id]
        return board

    def delete_board(self, board_id: str) -> None:
        board = self.get_board(board_id)

        for task_lists in board.lists.values():
            task_lists.cards.clear()

        board.lists.clear()
        del self.boards[board_id]

    def create_list(self, board_id: str, name: str) -> TaskList:
        if not name.strip():
            raise ValueError("List name cannot be empty.")

        board = self.get_board(board_id)
        list_id = generate_id()
        task_list = TaskList(id=list_id, name=name)
        board.lists[list_id] = task_list
        return task_list

    def find_list(self, list_id: str) -> tuple[Board, TaskList]:
        for board in self.boards.values():
            task_list = board.lists.get(list_id)
            if task_list is not None:
                return board, task_list

        raise ValueError(f"List with ID {list_id} does not exist.")

    def get_list(self, list_id: str) -> TaskList:
        _, task_list = self.find_list(list_id)
        return task_list

    def update_list(self, list_id: str, attribute: str, value: str) -> TaskList:
        _, task_list = self.find_list(list_id)

        if attribute == "name":
            if not value.strip():
                raise ValueError("List name cannot be empty.")
            task_list.name = value

        else:
            raise ValueError(f"Invalid attribute: {attribute}.")

        return task_list

    def delete_list(self, list_id: str) -> None:
        board, task_list = self.find_list(list_id)

        task_list.cards.clear()
        del board.lists[list_id]

    def create_card(self, list_id: str, name: str, description: str = "") -> Card:
        task_list = self.get_list(list_id)

        if not name.strip():
            raise ValueError("Card name cannot be empty.")

        card_id = generate_id()
        card = Card(id=card_id, name=name, description=description)
        task_list.cards[card_id] = card
        return card

    def find_card(self, card_id: str) -> tuple[Board, TaskList, Card]:
        for board in self.boards.values():
            for task_list in board.lists.values():
                card = task_list.cards.get(card_id)
                if card is not None:
                    return board, task_list, card

        raise ValueError(f"Card with ID {card_id} does not exist.")

    def get_card(self, card_id: str) -> Card:
        _, _, card = self.find_card(card_id)
        return card

    def update_card(self, card_id: str, attribute: str, value: str) -> Card:
        _, _, card = self.find_card(card_id)

        if attribute == "name":
            if not value.strip():
                raise ValueError("Card name cannot be empty.")
            card.name = value
        elif attribute == "description":
            card.description = value
        else:
            raise ValueError(f"Invalid attribute: {attribute}.")
        return card

    def assign_card(self, card_id: str, user_id: str) -> Card:
        board, _, card = self.find_card(card_id)
        user = self.get_user(user_id)

        if user_id not in board.members:
            raise ValueError(f"User with ID {user_id} is not a member of the board.")

        if card.assigned_user is not None and card.assigned_user.user_id == user_id:
            raise ValueError(
                f"Card with ID {card_id} is already assigned to user with ID {user_id}."
            )

        card.assigned_user = user
        return card

    def unassign_card(self, card_id: str) -> Card:
        card = self.get_card(card_id)
        card.assigned_user = None
        return card

    def delete_card(self, card_id: str) -> None:
        _, task_list, _ = self.find_card(card_id)
        del task_list.cards[card_id]

    def move_card(self, card_id: str, destination_list_id: str) -> Card:
        source_board, source_task_list, card = self.find_card(card_id)
        destination_board, destination_task_list = self.find_list(destination_list_id)

        if source_board.id != destination_board.id:
            raise ValueError("Cannot move card to a list in a different board.")

        if source_task_list.id == destination_task_list.id:
            return card

        del source_task_list.cards[card_id]
        destination_task_list.cards[card_id] = card

        return card

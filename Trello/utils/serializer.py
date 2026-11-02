from models.board import Board
from models.task_list import TaskList
from models.card import Card
from models.user import User


def user_to_dict(user: User) -> dict:
    return {
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
    }


def card_to_dict(card: Card) -> dict:
    result = {
        "id": card.id,
        "name": card.name,
        "description": card.description,
        "assignedTo": (
            user_to_dict(card.assigned_user) if card.assigned_user else None
        ),
    }
    return result


def list_to_dict(task_list: TaskList) -> dict:
    return {
        "id": task_list.id,
        "name": task_list.name,
        "cards": [card_to_dict(card) for card in task_list.cards.values()],
    }


def board_to_dict(board: Board) -> dict:
    return {
        "id": board.id,
        "name": board.name,
        "privacy": board.privacy.value,
        "url": board.url,
        "members": [user_to_dict(user) for user in board.members.values()],
        "lists": [list_to_dict(task_list) for task_list in board.lists.values()],
    }

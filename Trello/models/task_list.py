from dataclasses import dataclass, field

from models.card import Card


@dataclass
class TaskList:
    id: str
    name: str
    cards: dict[str, Card] = field(default_factory=dict)

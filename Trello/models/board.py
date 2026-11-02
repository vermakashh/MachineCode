from dataclasses import dataclass, field
from enum import Enum

from models.user import User
from models.task_list import TaskList


class Privacy(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


@dataclass
class Board:
    id: str
    name: str
    url: str
    privacy: Privacy = Privacy.PUBLIC
    members: dict[str, User] = field(default_factory=dict)
    lists: dict[str, TaskList] = field(default_factory=dict)

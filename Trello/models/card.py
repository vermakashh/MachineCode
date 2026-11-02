from dataclasses import dataclass
from typing import Optional

from models.user import User


@dataclass
class Card:
    id: str
    name: str
    description: str = ""
    assigned_user: Optional[User] = None

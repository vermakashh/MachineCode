from dataclasses import dataclass

from models.color import Color


@dataclass(frozen=True)
class Player:
    color: Color

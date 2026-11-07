from enum import Enum


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

    def opposite(self) -> "Color":
        return Color.BLACK if self == Color.WHITE else Color.WHITE

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def is_valid(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.col < 8

    @classmethod
    def from_notation(cls, notation: str) -> "Position":
        if len(notation) != 2:
            raise ValueError("Invalid chess position")

        file, rank = notation[0], notation[1]

        if file not in "abcdefgh" or rank not in "12345678":
            raise ValueError("Invalid chess position")

        col = ord(file) - ord("a")
        row = 8 - int(rank)

        return cls(row, col)

    def to_notation(self) -> str:
        if not self.is_valid():
            raise ValueError("Position is outside the board")

        file = chr(ord("a") + self.col)
        rank = str(8 - self.row)

        return file + rank

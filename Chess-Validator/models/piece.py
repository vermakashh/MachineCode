from abc import ABC, abstractmethod

from models.color import Color
from models.position import Position


class Piece(ABC):
    def __init__(self, color: Color, position: Position):
        self.color = color
        self.position = position

    @abstractmethod
    def can_move(self, destination: Position, board) -> bool:
        pass

    def can_capture_or_move_to(self, destination: Position, board) -> bool:
        if not destination.is_valid():
            return False

        target = board.get_piece(destination)

        if target is not None and target.color == self.color:
            return False

        return True

    def is_path_clear(self, destination: Position, board) -> bool:
        row_diff = destination.row - self.position.row
        col_diff = destination.col - self.position.col

        row_steps = (row_diff > 0) - (row_diff < 0)
        col_steps = (col_diff > 0) - (col_diff < 0)

        row = self.position.row + row_steps
        col = self.position.col + col_steps

        while (row, col) != (destination.row, destination.col):
            position = Position(row, col)

            if board.get_piece(position) is not None:
                return False

            row += row_steps
            col += col_steps

        return True

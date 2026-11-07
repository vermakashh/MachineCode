from models.color import Color
from models.piece import Piece


class Pawn(Piece):
    def can_move(self, destination, board) -> bool:
        if not destination.is_valid():
            return False

        row_diff = destination.row - self.position.row
        col_diff = destination.col - self.position.col

        direction = -1 if self.color == Color.WHITE else 1

        target = board.get_piece(destination)

        # Straight movement: destination must be empty.
        if col_diff == 0:
            if target is not None:
                return False

            # One square forward.
            if row_diff == direction:
                return True

            # Two squares forward from the starting rank.
            start_row = 6 if self.color == Color.WHITE else 1

            if self.position.row == start_row and row_diff == 2 * direction:
                intermediate = type(self.position)(
                    self.position.row + direction,
                    self.position.col,
                )

                return board.get_piece(intermediate) is None

            return False

        # Diagonal movement: must capture an opponent.
        if abs(col_diff) == 1 and row_diff == direction:
            return target is not None and target.color != self.color

        return False

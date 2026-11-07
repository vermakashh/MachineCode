from models.piece import Piece


class King(Piece):
    def can_move(self, destination, board) -> bool:
        if not self.can_capture_or_move_to(destination, board):
            return False

        row_diff = abs(destination.row - self.position.row)
        col_diff = abs(destination.col - self.position.col)

        return max(row_diff, col_diff) == 1

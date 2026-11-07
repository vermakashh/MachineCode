from models.piece import Piece


class Rook(Piece):
    def can_move(self, destination, board) -> bool:
        if not self.can_capture_or_move_to(destination, board):
            return False

        row_diff = abs(destination.row - self.position.row)
        col_diff = abs(destination.col - self.position.col)

        if (row_diff == 0) == (col_diff == 0):
            return False

        return self.is_path_clear(destination, board)

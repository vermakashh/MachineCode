from models.piece import Piece


class Bishop(Piece):
    def can_move(self, destination, board) -> bool:
        if not self.can_capture_or_move_to(destination, board):
            return False

        row_diff = abs(destination.row - self.position.row)
        col_diff = abs(destination.col - self.position.col)

        if row_diff == 0 or row_diff != col_diff:
            return False

        return self.is_path_clear(destination, board)

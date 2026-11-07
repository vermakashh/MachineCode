from models.piece import Piece


class Knight(Piece):
    def can_move(self, destination, board) -> bool:
        if not self.can_capture_or_move_to(destination, board):
            return False

        row_diff = abs(destination.row - self.position.row)
        col_diff = abs(destination.col - self.position.col)

        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

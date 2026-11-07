from models.piece import Piece


class Queen(Piece):
    def can_move(self, destination, board) -> bool:
        if not self.can_capture_or_move_to(destination, board):
            return False

        row_diff = abs(destination.row - self.position.row)
        col_diff = abs(destination.col - self.position.col)

        if row_diff == 0 and col_diff == 0:
            return False

        is_straight = row_diff == 0 or col_diff == 0
        is_diagonal = row_diff == col_diff

        if not (is_straight or is_diagonal):
            return False

        return self.is_path_clear(destination, board)

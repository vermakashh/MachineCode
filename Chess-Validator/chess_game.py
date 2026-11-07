from board import Board
from models.color import Color
from models.position import Position
from player import Player


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.players = {
            Color.WHITE: Player(Color.WHITE),
            Color.BLACK: Player(Color.BLACK),
        }
        self.current_turn = Color.WHITE

    def make_move(self, source, destination) -> bool:
        piece = self.board.get_piece(source)

        # The source square must contain a piece.
        if piece is None:
            return False

        # The piece must belong to the current player.
        if piece.color != self.current_turn:
            return False

        # Validate and execute the move.
        if not self.board.move_piece(source, destination):
            return False

        # Change turns only after a successful move.
        self.current_turn = self.current_turn.opposite()

        return True

    def display_board(self):
        self.board.display()

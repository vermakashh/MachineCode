from models.color import Color
from models.position import Position
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._initialize_board()

    def _initialize_board(self):
        # Black pieces occupy ranks 8 and 7.
        self._place_back_rank(Color.BLACK, 0)
        self._place_pawns(Color.BLACK, 1)

        # White pieces occupy ranks 1 and 2.
        self._place_pawns(Color.WHITE, 6)
        self._place_back_rank(Color.WHITE, 7)

    def _place_pawns(self, color, row):
        for col in range(8):
            position = Position(row, col)
            self.grid[row][col] = Pawn(color, position)

    def _place_back_rank(self, color, row):
        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for col, piece_class in enumerate(piece_classes):
            position = Position(row, col)
            self.grid[row][col] = piece_class(color, position)

    def get_piece(self, position):
        if not position.is_valid():
            return None

        return self.grid[position.row][position.col]

    def move_piece(self, source, destination):
        piece = self.get_piece(source)

        if piece is None:
            return False

        if not piece.can_move(destination, self):
            return False

        self.grid[destination.row][destination.col] = piece
        self.grid[source.row][source.col] = None
        piece.position = destination

        return True

    def display(self):
        for row in range(8):
            rank = 8 - row
            symbols = []

            for col in range(8):
                piece = self.grid[row][col]

                if piece is None:
                    symbols.append("..")
                else:
                    symbol = type(piece).__name__[0].upper()

                    if isinstance(piece, Knight):
                        symbol = "N"

                    prefix = "W" if piece.color == Color.WHITE else "B"

                    symbols.append(prefix + symbol)

            print(f"{rank} " + " ".join(symbols))

        print("  " + " ".join(f"{f} " for f in "abcdefgh"))

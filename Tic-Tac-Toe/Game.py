from Board import Board


class Game:
    def __init__(self, players, board_size=3):
        if len(players) < 2:
            raise ValueError("players must be equal or more than 2")

        symbols = [player.symbol for player in players]

        if len(set(symbols)) != len(symbols):
            raise ValueError("each player must have unique symbol")
        if "-" in symbols:
            raise ValueError(" The '-' symbol is reserved for empty slots of the board")

        self.players = players
        self.current_player_index = 0
        self.board = Board(board_size)
        self.game_over = False

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_move(self, row, col):
        player = self.current_player

        # Validate the move
        if not self.board.is_valid_move(row, col):
            print("Invalid Move")
            return

        # Place the piece
        self.board.place_piece(row, col, player.symbol)

        # Display the board
        self.board.display()

        # Check for winner
        if self.board.has_winner(player.symbol):
            self.game_over = True
            print(f"{player.name} won the game")
            return True

        # check for draw
        if self.board.is_full():
            self.game_over = True
            print("The game is a draw")
            return

        self.switch_turn()

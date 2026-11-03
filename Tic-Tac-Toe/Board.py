class Board:
    def __init__(self, size=3):
        if size < 1:
            raise ValueError("Board size must be positive")

        self.size = size
        self.grid = [["-" for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        for row in self.grid:
            print(" ".join(row))

    def is_valid_move(self, row, col):
        # Adjust for 0-based indexing
        row -= 1
        col -= 1
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        return self.grid[row][col] == "-"

    def place_piece(self, row, col, symbol):
        # Adjust for 0-based indexing
        row -= 1
        col -= 1
        self.grid[row][col] = symbol

    def is_full(self):
        return all(cell != "-" for row in self.grid for cell in row)

    def has_winner(self, symbol):
        # check rows
        for row in self.grid:
            if all(cell == symbol for cell in row):
                return True

        # check columns
        for col in range(self.size):
            if all(self.grid[row][col] == symbol for row in range(self.size)):
                return True

        # check diagonals
        if all(self.grid[i][i] == symbol for i in range(self.size)):
            return True

        # check anti-diagonol
        if all(self.grid[i][self.size - 1 - i] == symbol for i in range(self.size)):
            return True

        return False

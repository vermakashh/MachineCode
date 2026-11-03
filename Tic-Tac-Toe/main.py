from Players import Player
from Game import Game


def read_line(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return None


def read_player_count():
    while True:
        line = read_line("Enter number of players: ")
        if line is None or line.lower() == "exit":
            return None

        if not line.isdigit() or int(line) < 2:
            print("At least 2 players are required to start the game")
            continue

        return int(line)


def read_players(count):
    players = []

    while len(players) < count:
        line = read_line(f"Enter symbol and name for player {len(players) + 1}: ")
        if line is None or line.lower() == "exit":
            return None

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print("Invalid input, expected: <symbol> <name>")
            continue

        symbol, name = parts
        if symbol == "-":
            print("The '-' symbol is reserved for empty slots of the board")
            continue
        if any(player.symbol == symbol for player in players):
            print(f"The symbol '{symbol}' is already taken")
            continue

        players.append(Player(name, symbol))

    return players


def main():
    board_size = 3

    count = read_player_count()
    if count is None:
        return

    players = read_players(count)
    if players is None:
        return

    try:
        game = Game(players, board_size)
    except ValueError as error:
        print(error)
        return

    # Display the board
    game.board.display()

    # Read moves until the game ends
    while not game.game_over:
        player = game.current_player
        line = read_line(f"{player.name} ({player.symbol}) - enter row and col: ")

        if line is None:
            break
        if line.lower() == "exit":
            print("Game exited")
            break

        try:
            row, col = map(int, line.split())
        except ValueError:
            print("Invalid Move")
            continue

        game.play_move(row, col)


if __name__ == "__main__":
    main()

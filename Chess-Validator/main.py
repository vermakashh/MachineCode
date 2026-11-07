from chess_game import ChessGame
from models.position import Position


def main():
    game = ChessGame()
    game.display_board()

    while True:
        try:
            user_input = input().strip()

            if user_input.lower() == "exit":
                break

            parts = user_input.split()

            if len(parts) != 2:
                print("Invalid Move")
                continue

            source = Position.from_notation(parts[0])
            destination = Position.from_notation(parts[1])

            if game.make_move(source, destination):
                game.display_board()
            else:
                print("Invalid Move")

        except ValueError:
            print("Invalid Move")
        except EOFError:
            break


if __name__ == "__main__":
    main()

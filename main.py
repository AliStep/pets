from game import Game
from gui import GameGUI


def on_move(row, col):
    return game.try_move(row, col)


if __name__ == "__main__":
    game = Game()
    gui = GameGUI(game, on_move)
    gui.run()
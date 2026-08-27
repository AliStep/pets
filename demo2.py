"""Демо 2: птенчик доходит до зерна и игра заканчивается победой.

Зерно лежит на клетке (3,5) с самого начала и не двигается.
Птенчик по соседним клеткам доходит до него -> модальное окно победы.
После нажатия «ОК» стартует новая игра и демо закрывается.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game
from gui import GameGUI, CELL

STEP_MS = 700


class _ClickEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Demo2:
    def __init__(self):
        self.game = Game()
        # Зерно лежит на месте с самого начала — птенчик доходит до него
        self.game.grain.row, self.game.grain.col = 3, 5
        self.gui = GameGUI(self.game, self.game.try_move)
        self.gui._draw_all()
        self.root = self.gui.root
        self.root.title("Демо 2: дойти до зерна и победить")
        self.route = [(2, 3), (2, 4), (3, 4), (3, 5)]
        self.root.after(600, self._act)
        self.root.mainloop()

    def _click_pos(self, row, col):
        x = col * CELL + CELL // 2
        y = row * CELL + CELL // 2
        return x, y

    def _act(self):
        if self.route:
            row, col = self.route.pop(0)
            self.root.title(f"Демо 2: птенчик идёт на ({row},{col})")
            self.gui._on_click(_ClickEvent(*self._click_pos(row, col)))
            # последняя клетка маршрута — зерно, поэтому после неё финиш
            if not self.route:
                self.root.title("Демо 2 завершено")
                self.root.after(1500, self.root.destroy)
            else:
                self.root.after(STEP_MS, self._act)
            return

        # маршрут пуст — не должно сюда попадать
        self.root.destroy()


if __name__ == "__main__":
    Demo2()
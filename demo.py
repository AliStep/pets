"""Демо-прогон игры с видимым окном.

Открывает GUI и пошагово выполняет сценарии, двигая птенчика «кликами»
по соседним клеткам. Показывает выбор клеток и смену положений.
Окно закрывается само по завершении всех сценариев.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game
from gui import GameGUI, CELL

STEP_MS = 700  # задержка между шагами для наглядности


class _ClickEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Demo:
    def __init__(self):
        self.game = Game()
        self.gui = GameGUI(self.game, self.game.try_move)
        self.root = self.gui.root
        self.root.title("Демо игры «Покорми птенчика»")
        self.steps = self._build_scenarios()
        self.root.after(600, self._run_next)
        self.root.mainloop()

    def _build_scenarios(self):
        steps = []
        route = [
            (2, 3), (2, 4), (1, 4), (1, 3), (0, 3), (0, 2),
            (1, 2), (1, 1), (2, 1), (2, 0), (3, 0), (3, 1),
            (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (3, 3), (2, 3),
        ]
        for r, c in route:
            steps.append((f"Клик на клетку ({r},{c})", (r, c)))
        return steps

    def _click_pos(self, row, col):
        x = col * CELL + CELL // 2
        y = row * CELL + CELL // 2
        return x, y

    def _run_next(self):
        if not self.steps:
            self.root.title("Демо завершено")
            self.root.after(1200, self.root.destroy)
            return
        label, cell = self.steps.pop(0)
        self.root.title(f"Демо: {label}")
        self.root.update()
        x, y = self._click_pos(*cell)
        self.gui._on_click(_ClickEvent(x, y))
        self.root.update()
        self.root.after(STEP_MS, self._run_next)


if __name__ == "__main__":
    Demo()
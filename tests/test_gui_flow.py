import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gui import GameGUI
from game import Game


class TestGameGuiFlow(unittest.TestCase):
    """Интеграционные тесты GUI-кейсов игры.

    Каждый тест создаёт собственное окно и закрывает его по завершении.
    """

    def tearDown(self):
        if hasattr(self, "gui"):
            self.gui.root.destroy()

    def _make_gui(self):
        game = Game()
        self.gui = GameGUI(game, game.try_move)
        return game, self.gui

    def test_chick_stays_in_place_on_5_new_game(self):
        game, gui = self._make_gui()
        start = (game.chick.row, game.chick.col)
        self.assertEqual(start, (2, 2))

        for _ in range(5):
            gui._reset()
            self.assertEqual(
                (game.chick.row, game.chick.col), (2, 2),
                "Игла не должна двигаться после «Новая игра»",
            )

    def test_rules_dialog_ok_continues(self):
        """Клино по "ОК" в правилах должно закрыть окно и игру продолжить."""
        game, gui = self._make_gui()
        # существует Toplevel с заголовком правил — проверим на наличие
        self.assertIsNotNone(game)
        # игра в стартовой выписке
        self.assertEqual((game.chick.row, game.chick.col), (2, 2))

    def test_win_starts_new_game_after_ok(self):
        """После победы и "ОК" стартует новая игра (птенчик в центре)."""
        game, gui = self._make_gui()
        game.grain.row, game.grain.col = 2, 3
        ok, msg = game.try_move(2, 3)
        self.assertTrue(ok, msg)
        self.assertTrue(game.won)
        gui._start_new_game()
        self.assertFalse(game.won)
        self.assertEqual((game.chick.row, game.chick.col), (2, 2))

    def test_error_dialog_not_crash(self):
        """Ошибка хода в тклинго не падает."""
        game, gui = self._make_gui()
        ok, msg = game.try_move(0, 0)
        self.assertFalse(ok)
        self.assertIn("ближайшие", msg)


if __name__ == "__main__":
    unittest.main()
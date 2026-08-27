import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game import Game, SIZE, Chick, Grain


class TestGameInit(unittest.TestCase):
    def test_chick_starts_at_center(self):
        g = Game()
        self.assertEqual((g.chick.row, g.chick.col), (2, 2))

    def test_grain_not_on_chick(self):
        for _ in range(100):
            g = Game()
            self.assertNotEqual(
                (g.grain.row, g.grain.col), (g.chick.row, g.chick.col)
            )

    def test_grain_on_board(self):
        g = Game()
        self.assertTrue(0 <= g.grain.row < SIZE)
        self.assertTrue(0 <= g.grain.col < SIZE)

    def test_game_starts_not_won(self):
        g = Game()
        self.assertFalse(g.won)


class TestAdjacency(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.chick = Chick(2, 2)

    def test_adjacent_up(self):
        self.assertTrue(self.game.is_adjacent(1, 2))

    def test_adjacent_down(self):
        self.assertTrue(self.game.is_adjacent(3, 2))

    def test_adjacent_left(self):
        self.assertTrue(self.game.is_adjacent(2, 1))

    def test_adjacent_right(self):
        self.assertTrue(self.game.is_adjacent(2, 3))

    def test_not_adjacent_diagonal(self):
        self.assertFalse(self.game.is_adjacent(1, 1))
        self.assertFalse(self.game.is_adjacent(1, 3))
        self.assertFalse(self.game.is_adjacent(3, 1))
        self.assertFalse(self.game.is_adjacent(3, 3))

    def test_not_adjacent_jump(self):
        self.assertFalse(self.game.is_adjacent(0, 2))
        self.assertFalse(self.game.is_adjacent(2, 4))
        self.assertFalse(self.game.is_adjacent(4, 2))

    def test_not_adjacent_far(self):
        self.assertFalse(self.game.is_adjacent(0, 0))
        self.assertFalse(self.game.is_adjacent(5, 5))

    def test_not_adjacent_same_cell(self):
        self.assertFalse(self.game.is_adjacent(2, 2))


class TestOnBoard(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_on_board_center(self):
        self.assertTrue(self.game.is_on_board(2, 2))

    def test_on_board_edges(self):
        self.assertTrue(self.game.is_on_board(0, 0))
        self.assertTrue(self.game.is_on_board(5, 5))
        self.assertTrue(self.game.is_on_board(0, 5))
        self.assertTrue(self.game.is_on_board(5, 0))

    def test_off_board_negative(self):
        self.assertFalse(self.game.is_on_board(-1, 0))
        self.assertFalse(self.game.is_on_board(0, -1))

    def test_off_board_too_high(self):
        self.assertFalse(self.game.is_on_board(6, 0))
        self.assertFalse(self.game.is_on_board(0, 6))


class TestMove(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.chick = Chick(2, 2)

    def test_move_adjacent_right(self):
        ok, msg = self.game.try_move(2, 3)
        self.assertTrue(ok)
        self.assertEqual((self.game.chick.row, self.game.chick.col), (2, 3))

    def test_move_adjacent_up(self):
        ok, msg = self.game.try_move(1, 2)
        self.assertTrue(ok)
        self.assertEqual((self.game.chick.row, self.game.chick.col), (1, 2))

    def test_move_non_adjacent_returns_error(self):
        ok, msg = self.game.try_move(0, 0)
        self.assertFalse(ok)
        self.assertIn("ближайшие клетки", msg)
        self.assertEqual((self.game.chick.row, self.game.chick.col), (2, 2))

    def test_move_off_board_returns_false(self):
        ok, msg = self.game.try_move(-1, 2)
        self.assertFalse(ok)

    def test_move_off_board_empty_message(self):
        ok, msg = self.game.try_move(6, 2)
        self.assertEqual(msg, "")

    def test_move_chain(self):
        moves = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        for r, c in moves:
            ok, _ = self.game.try_move(r, c)
            self.assertTrue(ok, f"move to ({r},{c}) failed")
        self.assertEqual((self.game.chick.row, self.game.chick.col), (3, 4))

    def test_move_back_to_previous(self):
        self.game.try_move(2, 3)
        self.game.try_move(2, 2)
        self.assertEqual((self.game.chick.row, self.game.chick.col), (2, 2))


class TestWin(unittest.TestCase):
    def test_win_when_reaching_grain(self):
        g = Game()
        g.chick = Chick(2, 2)
        g.grain = Grain(2, 3)
        ok, msg = g.try_move(2, 3)
        self.assertTrue(ok)
        self.assertTrue(g.won)
        self.assertIn("молодец", msg)

    def test_not_win_on_ordinary_move(self):
        g = Game()
        g.chick = Chick(2, 2)
        g.grain = Grain(4, 4)
        ok, msg = g.try_move(2, 3)
        self.assertTrue(ok)
        self.assertFalse(g.won)
        self.assertEqual(msg, "")


class TestReset(unittest.TestCase):
    def test_reset_chick_returns_to_start(self):
        g = Game()
        g.try_move(2, 3)
        g.try_move(3, 3)
        g.reset()
        self.assertEqual((g.chick.row, g.chick.col), (2, 2))

    def test_reset_clears_win(self):
        g = Game()
        g.chick = Chick(2, 2)
        g.grain = Grain(2, 3)
        g.try_move(2, 3)
        self.assertTrue(g.won)
        g.reset()
        self.assertFalse(g.won)

    def test_reset_changes_grain_position(self):
        g = Game()
        old = (g.grain.row, g.grain.col)
        changed = False
        for _ in range(20):
            g.reset()
            if (g.grain.row, g.grain.col) != old:
                changed = True
                break
        self.assertTrue(changed, "grain should move after resets")

    def test_new_game_5_times_chick_stays(self):
        g = Game()
        for _ in range(5):
            g.reset()
            self.assertEqual((g.chick.row, g.chick.col), (2, 2))


class TestChickClass(unittest.TestCase):
    def test_move_to(self):
        c = Chick(1, 1)
        c.move_to(4, 5)
        self.assertEqual((c.row, c.col), (4, 5))


class TestGrainClass(unittest.TestCase):
    def test_grain_position(self):
        gr = Grain(3, 4)
        self.assertEqual((gr.row, gr.col), (3, 4))


if __name__ == "__main__":
    unittest.main()
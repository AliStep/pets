import random

SIZE = 6


class Chick:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def move_to(self, row: int, col: int):
        self.row = row
        self.col = col


class Grain:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col


class Game:
    def __init__(self):
        self.chick = Chick(2, 2)
        self.grain = self._place_grain()
        self.won = False

    def _place_grain(self) -> Grain:
        while True:
            r = random.randrange(SIZE)
            c = random.randrange(SIZE)
            if (r, c) != (self.chick.row, self.chick.col):
                return Grain(r, c)

    def is_adjacent(self, row: int, col: int) -> bool:
        dr = abs(row - self.chick.row)
        dc = abs(col - self.chick.col)
        return (dr == 1 and dc == 0) or (dr == 0 and dc == 1)

    def is_on_board(self, row: int, col: int) -> bool:
        return 0 <= row < SIZE and 0 <= col < SIZE

    def try_move(self, row: int, col: int) -> tuple[bool, str]:
        if not self.is_on_board(row, col):
            return False, ""

        if not self.is_adjacent(row, col):
            return False, "Ходить можно только на ближайшие клетки (вниз-вверх-влево-вправо)."

        self.chick.move_to(row, col)

        if (row, col) == (self.grain.row, self.grain.col):
            self.won = True
            return True, "Птенчик поел и доволен! Ты молодец!"

        return True, ""

    def reset(self):
        self.__init__()
from bitarray import bitarray
from random import randrange


class mybitarray(bitarray):

    def __lshift__(self, count):
        return self[count:] + type(self)('0') * count

    def __rshift__(self, count):
        return type(self)('0') * count + self[:-count]

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.to01())


class GameOfLifeCore(object):

    def __init__(self, cols, rows):
        self.mask = GameOfLifeMask(cols, rows)
        self.cols = cols
        self.rows = rows
        self.cells = mybitarray(cols * rows)
        self.cells.setall(False)

    def __getitem__(self, coords):
        index = coords[1] * self.cols + coords[0]
        return self.cells[index]

    def __setitem__(self, coords, value):
        index = coords[1] * self.cols + coords[0]
        self.cells[index] = value

    def reset(self):
        self.cells.setall(False)

    def next_step(self):
        self.cells = self.mask.down_right(self.cells)
        # self.cells = self.mask.down_left(self.cells)

    def randomize(self):
        length = self.cells.length()
        for i in range(length):
            self.cells[i] = randrange(100) > 80


class GameOfLifeMask:

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        self.left_mask = self._create_left()
        self.right_mask = self._create_right()
        self.up_mask = self._create_up()
        self.down_mask = self._create_down()
        self.up_left_mask = self.left_mask & self.up_mask
        self.down_left_mask = self.left_mask & self.down_mask
        self.up_right_mask = self.right_mask & self.up_mask
        self.down_right_mask = self.right_mask & self.down_mask

    def left(self, cells):
        return (cells << 1) & self.left_mask

    def right(self, cells):
        return (cells >> 1) & self.right_mask

    def up(self, cells):
        return (cells << self.cols) & self.up_mask

    def down(self, cells):
        return (cells >> self.cols) & self.up_mask

    def up_left(self, cells):
        return (cells << (self.cols + 1)) & self.up_left_mask

    def down_left(self, cells):
        return (cells >> (self.cols - 1)) & self.down_left_mask

    def up_right(self, cells):
        return (cells << (self.cols - 1)) & self.up_right_mask

    def down_right(self, cells):
        return (cells >> (self.cols + 1)) & self.down_right_mask

    def _create_left(self):
        mask = mybitarray(self.cols * self.rows)
        mask.setall(True)
        for i in range(self.rows):
            mask[(i + 1) * self.cols - 1] = False
        return mask

    def _create_right(self):
        mask = mybitarray(self.cols * self.rows)
        mask.setall(True)
        for i in range(self.rows):
            mask[i * self.cols] = False
        return mask

    def _create_up(self):
        mask = mybitarray(self.cols * self.rows)
        mask.setall(True)
        for i in range(self.cols):
            mask[-i] = False
        return mask

    def _create_down(self):
        mask = mybitarray(self.cols * self.rows)
        mask.setall(True)
        for i in range(self.cols):
            mask[i] = False
        return mask

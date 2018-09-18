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
        # self.cells = self.mask.left(self.cells)
        # self.cells = self.mask.up_left(self.cells)
        self.cells = self.mask.down_left(self.cells)

    def randomize(self):
        length = self.cells.length()
        for i in range(length):
            self.cells[i] = randrange(100) > 80


class GameOfLifeMask:

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        self.left_mask = self._create_left()
        self.up_left_mask = self._create_up_left()
        self.down_left_mask = self._create_down_left()

    def left(self, cells):
        return (cells << 1) & self.left_mask

    def up_left(self, cells):
        return (cells << (self.cols + 1)) & self.up_left_mask

    def down_left(self, cells):
        return (cells >> (self.cols - 1)) & self.down_left_mask

    def right(self, cells):
        pass

    def up_right(self, cells):
        pass

    def down_right(self, cells):
        pass

    def up(self, cells):
        pass

    def down(self, cells):
        pass

    def _create_left(self):
        mask = mybitarray(self.cols * self.rows)
        mask.setall(True)
        for i in range(self.rows):
            mask[(i + 1) * self.cols - 1] = False
        return mask

    def _create_up_left(self):
        mask = self._create_left()
        for i in range(self.cols):
            mask[-i] = False
        return mask

    def _create_down_left(self):
        mask = self._create_left()
        for i in range(self.cols):
            mask[i] = False
        return mask

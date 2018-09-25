from bitarray import bitarray
from random import randrange


class mybitarray(bitarray):

    def __lshift__(self, count):
        return self[count:] + type(self)('0') * count

    def __rshift__(self, count):
        return type(self)('0') * count + self[:-count]

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.to01())


class Core(object):

    def __init__(self, cols, rows):
        self.mask = Mask(cols, rows)
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

    def count_of(self, state):
        return self.cells.count(state)

    def next_step(self):
        c = [self.mask.left(self.cells)]
        c.append(self.mask.right(self.cells))
        c.append(self.mask.up(self.cells))
        c.append(self.mask.down(self.cells))
        c.append(self.mask.up_left(self.cells))
        c.append(self.mask.down_left(self.cells))
        c.append(self.mask.up_right(self.cells))
        c.append(self.mask.down_right(self.cells))

        s0 = ~(c[0] | c[1])
        s1 = c[0] ^ c[1]
        s2 = c[0] & c[1]
        s3 = mybitarray(self.cols * self.rows)
        s3.setall(False)

        for _c in c[2:]:
            s3 = (s3 & ~_c) | (s2 & _c)
            s2 = (s2 & ~_c) | (s1 & _c)
            s1 = (s1 & ~_c) | (s0 & _c)
            s0 = s0 & ~_c

        self.cells = (~self.cells & s3) | (self.cells & (s2 | s3))

    def randomize(self):
        length = self.cells.length()
        for i in range(length):
            self.cells[i] = randrange(100) > 80


class Config:
    __speed = 5.0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        v = value
        if not isinstance(value, float):
            v = float(v)
        self.__speed = v


class Mask:

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

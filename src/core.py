from bitarray import bitarray
from random import randrange


class GameOfLifeCore(object):

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.cells = bitarray(cols * rows)
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
        pass

    def randomize(self):
        length = self.cells.length()
        for i in range(length):
            self.cells[i] = randrange(100) > 80

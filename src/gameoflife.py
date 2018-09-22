import os
import random
import timeit
from itertools import product

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.logger import Logger
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from core import GameOfLifeCore
from util import *


class Panel(BoxLayout):

    @register_event
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_core(self, core):
        self.core = core


class OperatePanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_menu(self):
        pass

    def on_play(self):
        pass

    def on_stop(self):
        pass


class MenuPanel(Panel):

    def __init__(self, **kwargs):
        super(MenuPanel, self).__init__(**kwargs)
        self.state = 0

    def toggle(self, ed):
        state_list = ['in', 'out']
        method = 'slide_{}'.format(state_list[self.state])
        getattr(self, method)()
        self.state = (self.state + 1) % 2

    def slide_in(self):
        animation = Animation(
            pos_hint={'right': 1},
            duration=0.5,
            transition='out_cubic'
        )
        animation.start(self)

    def slide_out(self):
        animation = Animation(
            pos_hint={'right': 2},
            duration=0.5,
            transition='in_cubic'
        )
        animation.start(self)


class CellGridPanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def random_init(self, obj):
        self.core.randomize()
        self.update_grid()

    def next_step(self, obj):
        self.core.next_step()
        self.update_grid()

    def update_grid(self):
        self.canvas.clear()
        w, h = self.size[0] / self.core.cols, self.size[1] / self.core.rows
        with self.canvas:
            Color(0, 1, 0, 0.8)
            field = list(product(range(self.core.cols), range(self.core.rows)))
            cells = map(lambda coords: self.create_cell(*coords, w, h), field)
            [c for c in cells if c is not None]

    def create_cell(self, x, y, w, h):
            if self.core[x, y]:
                _x = x * w + self.pos[0]
                _y = self.height - (y + 1) * h + self.pos[1]
                return Ellipse(size=(w, h), pos=(_x, _y))


class GameOfLife(BoxLayout):
    core = GameOfLifeCore(120, 80)
    cell_grid = ObjectProperty()
    operate = ObjectProperty()
    menu = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_core()
        self.operate.bind(on_menu=self.menu.toggle)
        self.operate.bind(on_play=self.cell_grid.random_init)
        self.operate.bind(on_stop=self.cell_grid.next_step)

    # Panelクラスを継承しているクラスにcoreをセットする
    def set_core(self):
        for key in GameOfLife.__dict__.keys():
            panel = getattr(self, key)
            if isinstance(panel, Panel):
                panel.set_core(self.core)


class GameOfLifeApp(App):

    def build(self):
        return GameOfLife()


if __name__ == '__main__':
    resource_add_path(resource_path())

    cur_path = os.path.dirname(os.path.abspath(__file__))
    load_style(cur_path + '/layouts/*')

    GameOfLifeApp().run()

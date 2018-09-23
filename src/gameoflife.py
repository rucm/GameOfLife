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
        self.ids['play'].disabled = True
        self.ids['stop'].disabled = False

    def on_stop(self):
        self.ids['play'].disabled = False
        self.ids['stop'].disabled = True

    def on_random(self):
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

    def play(self, obj):
        self.event = Clock.schedule_interval(self.next_step, 0.5)

    def stop(self, obj):
        Clock.unschedule(self.event)

    def random(self, obj):
        self.core.randomize()
        self.update_grid()

    def next_step(self, t):
        self.core.next_step()
        self.update_grid()

    def update_grid(self):
        self.canvas.clear()
        cols, rows = self.core.cols, self.core.rows
        size = self.size[0] / cols, self.size[1] / rows
        with self.canvas:
            Color(0, 1, 0, 0.8)
            field = list(product(range(cols), range(rows)))
            cells = map(lambda p: self.create_cell(*p, *size), field)
            list(cells)

    def create_cell(self, x, y, w, h):
        if self.core[x, y]:
            _x = x * w + self.pos[0]
            _y = self.height - (y + 1) * h + self.pos[1]
            return Ellipse(size=(w, h), pos=(_x, _y))


class GameOfLife(BoxLayout):
    core = GameOfLifeCore(60, 40)
    cell_grid = ObjectProperty()
    operate = ObjectProperty()
    menu = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_core()
        self.operate.bind(on_play=self.cell_grid.play)
        self.operate.bind(on_stop=self.cell_grid.stop)
        self.operate.bind(on_random=self.cell_grid.random)
        self.operate.bind(on_menu=self.menu.toggle)

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

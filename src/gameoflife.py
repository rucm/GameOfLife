import os
import timeit
from itertools import product

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty
)
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from util import *


class Panel(BoxLayout):
    pass


class OperatePanel(Panel):

    @register_event
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_menu(self):
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


class Cell(Image):
    state = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CellGrid(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 60
        self.rows = 40
        self.init_cells()
        # Clock.schedule_once(self.schedule, 1)

    def schedule(self, dt):
        result = timeit.timeit(self.init_cells, number=1)
        Logger.info('Draw cells: {}'.format(result))

    def init_cells(self):
        for x, y in product(range(self.cols), range(self.rows)):
            cell = Cell()
            cell.state = (x * y) % 2
            self.add_widget(cell)


class GameOfLife(BoxLayout):
    operate_panel = ObjectProperty()
    menu_panel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operate_panel.bind(on_menu=self.menu_panel.toggle)


class GameOfLifeApp(App):

    def build(self):
        return GameOfLife()


if __name__ == '__main__':
    resource_add_path(resource_path())

    cur_path = os.path.dirname(os.path.abspath(__file__))
    load_style(cur_path + '/layouts/*')

    GameOfLifeApp().run()

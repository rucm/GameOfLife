import os
from itertools import product

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout

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


class GameOfLifePanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_cells, 1)

    def init_cells(self, dt):
        row, col = int(self.height / 10), int(self.width / 10)
        with self.canvas:
            Color(0, 1, 0, 0.8)
            for x, y in product(range(col), range(row)):
                pos = (x * 9 + self.pos[0] + 1, y * 9 + self.pos[1] + 1)
                Rectangle(size=(8, 8), pos=pos)


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

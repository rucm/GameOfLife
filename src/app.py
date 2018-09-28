import os
import re
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
from kivy.uix.textinput import TextInput

import gameoflife as gol
from settings import general
from util import *


class Panel(BoxLayout):

    @register_event
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_core(self, core):
        self.core = core

    def set_config(self, config):
        self.config = config

    def set_info(self, info):
        self.info = info

    # イベント名と同名のメソッドを検索してバインド
    def bind_all(self, obj):
        for e in self.event_list:
            _e = e.lstrip('on_')
            if _e not in dir(obj):
                continue
            self.bind(**{e: getattr(obj, _e)})


class OperatePanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_play(self):
        self.ids['play'].disabled = True
        self.ids['stop'].disabled = False

    def on_stop(self):
        self.ids['play'].disabled = False
        self.ids['stop'].disabled = True

    def on_randomize(self):
        pass

    def on_toggle_menu(self):
        pass


class MenuPanel(Panel):

    def __init__(self, **kwargs):
        super(MenuPanel, self).__init__(**kwargs)
        self.state = 0
        Clock.schedule_interval(self.update_info, 1)

    def set_config(self, config):
        super().set_config(config)

    def toggle(self):
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

    def update_info(self, t):
        for k, v in self.info.items():
            if k not in self.ids:
                continue
            self.ids[k].value = '{}'.format(v)


class CellGridPanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def play(self):
        self.event = Clock.schedule_interval(
            self.next_step,
            1.0 / self.config.speed
        )

    def stop(self):
        if self.event is not None:
            Clock.unschedule(self.event)

    def restart(self):
        self.stop()
        self.play()

    def randomize(self):
        self.core.randomize()
        self.update_grid()

    def next_step(self, t):
        self.core.next_step()
        self.update_grid()

    def update_grid(self):
        self.record_cells()
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

    def record_cells(self):
        self.info['living_cells'] = self.core.count_of(True)
        self.info['dead_cells'] = self.core.count_of(False)


class GameOfLife(BoxLayout):
    cell_grid = ObjectProperty()
    operate = ObjectProperty()
    menu = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operate.bind_all(self)

    # Panelクラスを継承しているクラスの初期化
    def initialize_panel(self, core, config, info):
        for key in GameOfLife.__dict__.keys():
            panel = getattr(self, key)
            if isinstance(panel, Panel):
                panel.set_core(core)
                panel.set_config(config)
                panel.set_info(info)

    def play(self, *args, **kwargs):
        self.cell_grid.play()

    def stop(self, *args, **kwargs):
        self.cell_grid.stop()

    def randomize(self, *args, **kwargs):
        self.cell_grid.randomize()

    def toggle_menu(self, *args, **kwargs):
        self.menu.toggle()


class GameOfLifeApp(App):
    gol_core = gol.Core()
    gol_config = gol.Config()
    gol_info = {}
    gameoflife = None

    def set_default_config(self):
        options = self.config.options('gameoflife')
        for op in options:
            v = self.config.get('gameoflife', op)
            setattr(self.gol_config, op, v)
            self.gol_info[op] = v

    def build(self):
        self.gameoflife = GameOfLife()
        self.set_default_config()
        self.gameoflife.initialize_panel(
            self.gol_core,
            self.gol_config,
            self.gol_info
        )
        return self.gameoflife

    def build_config(self, config):
        config.setdefaults('gameoflife', {
            'speed': 5,
            'cols': 60,
            'rows': 40
        })

    def build_settings(self, settings):
        settings.add_json_panel('Game', self.config, data=general)

    def on_config_change(self, config, section, key, value):
        Logger.debug('Config: {}:{}'.format(section, key))
        if config is not self.config:
            return
        setattr(self.gol_config, key, value)
        self.gol_info[key] = value


if __name__ == '__main__':
    resource_add_path(resource_path())

    cur_path = os.path.dirname(os.path.abspath(__file__))
    load_style(cur_path + '/layouts/*')

    GameOfLifeApp().run()

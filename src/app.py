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

    def initialize(self):
        pass

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

    def on_toggle_info(self):
        pass


class InfoPanel(Panel):
    toggle_state = 0

    def __init__(self, **kwargs):
        super(InfoPanel, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_info, 1)

    def set_config(self, config):
        super().set_config(config)

    def toggle_info(self, *args, **kwargs):
        state_list = ['in', 'out']
        method = 'slide_{}'.format(state_list[self.toggle_state])
        getattr(self, method)()
        self.toggle_state = (self.toggle_state + 1) % 2

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

    def initialize(self):
        self.bind(pos=self.update_grid, size=self.update_grid)

    def play(self, *args, **kwargs):
        self.update_cells_size()
        self.event = Clock.schedule_interval(
            self.next_step,
            1.0 / self.config.speed
        )

    def stop(self, *args, **kwargs):
        if self.event is not None:
            self.update_cells_size()
            Clock.unschedule(self.event)

    def restart(self, *args, **kwargs):
        self.stop()
        self.play()

    def randomize(self, *args, **kwargs):
        self.update_cells_size()
        self.core.randomize()
        self.update_grid()

    def next_step(self, *args, **kwargs):
        self.core.next_step()

        time = timeit.timeit(self.update_grid, number=1)
        self.info['update_grid'] = '{:.3f}'.format(time)
        self.update_grid()

    def record_cells(self):
        self.info['living_cells'] = self.core.count_of(True)
        self.info['dead_cells'] = self.core.count_of(False)

    def update_grid(self, *args, **kwargs):
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

    def update_cells_size(self, *args, **kwargs):
        cols_flag = self.core.cols != self.config.cols
        rows_flag = self.core.rows != self.config.rows
        if cols_flag or rows_flag:
            self.core.set_size(self.config.cols, self.config.rows)

    def update_rect(self, *args, **kwargs):
        Logger.debug('Rect')


class GameOfLife(BoxLayout):
    cell_grid = ObjectProperty()
    operate = ObjectProperty()
    info = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operate.bind_all(self.cell_grid)
        self.operate.bind_all(self.info)

    # Panelクラスを継承しているクラスの初期化
    def initialize_panel(self, core, config, info):
        for key in GameOfLife.__dict__.keys():
            panel = getattr(self, key)
            if isinstance(panel, Panel):
                panel.set_core(core)
                panel.set_config(config)
                panel.set_info(info)
                panel.initialize()


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

import os
import sys
import glob
import re
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path


def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_style(dir_path):
    """
    実行ファイルをカレントディレクトリとして、
    指定したディレクトリに存在するkvファイルを読み込む
    """
    cur_path = os.path.dirname(os.path.abspath(__file__))
    style_files = glob.glob('{}/{}'.format(cur_path, dir_path))
    for style in style_files:
        Builder.load_file(style)


def register_event(self):
    """
    'on_'で始まるメソッドを探してイベントとして登録する
    """
    pattern = re.compile('on_')
    event_list = [e for e in dir(self.__class__) if pattern.match(e)]
    for e in event_list:
        self.register_event_type(e)


class Panel(BoxLayout):
    pass


class OperatePanel(Panel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        register_event(self)

    def on_menu(self):
        pass


class MenuPanel(Panel):

    def toggle(self, ed):
        self.opacity = (self.opacity + 1) % 2
        self.disabled = not self.disabled


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
    load_style('layouts/*')

    GameOfLifeApp().run()

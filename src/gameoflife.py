import os
import sys
import glob
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.resources import resource_add_path


def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_style(dir_path):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    style_files = glob.glob('{}/{}'.format(cur_path, dir_path))
    for style in style_files:
        Builder.load_file(style)


class Panel(BoxLayout):
    pass


class OperatePanel(Panel):
    pass


class MenuPanel(Panel):
    pass


class GameOfLife(BoxLayout):
    pass


class GameOfLifeApp(App):

    def build(self):
        return GameOfLife()


if __name__ == '__main__':
    resource_add_path(resource_path())
    load_style('layouts/*')

    GameOfLifeApp().run()

import os
import sys
import glob
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


def resourcePath():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    cur_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_path)


def loadStyle(dir_path):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    style_files = glob.glob('{}/{}'.format(cur_path, dir_path))
    for style in style_files:
        Builder.load_file(style)


class GameOfLife(BoxLayout):
    pass


class GameOfLifeApp(App):

    def build(self):
        return GameOfLife()


if __name__ == '__main__':
    import kivy.resources
    kivy.resources.resource_add_path(resourcePath())
    loadStyle('layouts/*')
    GameOfLifeApp().run()

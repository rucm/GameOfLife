import os
import sys
import glob
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty


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


class SampleModal(ModalView):
    pass


class GameOfLife(BoxLayout):

    def modal(self):
        sample_modal = SampleModal()
        sample_modal.open()


class GameOfLifeApp(App):

    def build(self):
        return GameOfLife()


if __name__ == '__main__':
    import kivy.resources
    kivy.resources.resource_add_path(resourcePath())
    loadStyle('layouts/*')
    GameOfLifeApp().run()

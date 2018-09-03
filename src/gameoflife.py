import os
import sys
from kivy.app import App


def resourcePath():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.abspath('.'))


class GameOfLifeApp(App):
    pass


if __name__ == '__main__':
    import kivy.resources
    kivy.resources.resource_add_path(resourcePath())
    GameOfLifeApp().run()

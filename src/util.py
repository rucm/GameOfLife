import os
import sys
import glob
import re
from kivy.lang import Builder
from kivy.event import EventDispatcher


def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_style(dir_path):
    """
    指定したディレクトリに存在するkvファイルを読み込む
    """
    style_files = glob.glob(dir_path)
    for style in style_files:
        Builder.load_file(style)


def register_event(handler):
    """
    'on_'で始まるメソッドを探してイベントとして登録する
    __init__メソッドに付けるデコレータ
    """

    excludes = [
        'on_opacity',
        'on_touch_down',
        'on_touch_move',
        'on_touch_up'
    ]

    def wrapper(self, **kwargs):
        if not isinstance(self, EventDispatcher):
            raise TypeError('This class does not inherit EventDispatcher')
        pattern = re.compile('on_')
        event_list = [e for e in dir(self.__class__) if pattern.match(e)]
        event_list = [e for e in event_list if e not in excludes]
        for e in event_list:
            self.register_event_type(e)
        self.event_list = event_list
        return handler(self, **kwargs)

    return wrapper

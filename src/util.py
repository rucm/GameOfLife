import os
import sys
import glob
import re
from kivy.lang import Builder


def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_style(dir_path):
    """
    実行ファイルをカレントディレクトリとして、
    指定したディレクトリに存在するkvファイルを読み込む
    """
    print(__file__)
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

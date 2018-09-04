# Memo

## 別のkvファイルにスタイルを定義して使いたいとき

例えば以下のような構成になっている場合

- `test.kv`

```python
#:kivy 1.10

<Test@BoxLayout>:
    Button1:
        text: 'sample'
    Button2:
        text: 'sample'
```

- `buttons.kv`

```python
#:kivy 1.10

<Button1@Button>:
    background_color: 0, 1, 0, 0.8

<Button2@Button>:
    background_color: 0, 0, 1, 0.8
```

- `test.py`

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class Test(BoxLayout):
    pass


class TestApp(App):

    def build(self):
        return Test()


if __name__ == '__main__':
    Builder.load_file('./buttons.kv')
    TestApp().run()
```
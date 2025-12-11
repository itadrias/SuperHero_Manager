import widgets.config
from widgets.buttons import *
from kivy.app import App
from kivy.lang import Builder
import json

Builder.load_file("main.kv")

class MyApp(App):
    def build(self):
        return Main_Container()

MyApp().run()
from kivy.config import Config
from kivy.core.text import LabelBase

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set("graphics", "width", "950")
Config.set("graphics", "height", "540")
Config.set("graphics", "resizable", "0")

LabelBase.register(name='BebasNeue', fn_regular='resources/BebasNeue-Regular.ttf')
LabelBase.register(name='OpenSans', fn_regular='resources/OpenSans-Bold.ttf')
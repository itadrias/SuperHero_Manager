from kivy.config import Config
from kivy.core.text import LabelBase

# Configura el sistema de entrada para desactivar el multitáctil (emulación de mouse)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Establece las dimensiones de la ventana y bloquea el redimensionamiento
Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "540")
Config.set("graphics", "resizable", "0")

# Registra fuentes personalizadas para ser usadas en la aplicación
LabelBase.register(name='BebasNeue', fn_regular='resources/BebasNeue-Regular.ttf')
LabelBase.register(name='OpenSans', fn_regular='resources/OpenSans-Bold.ttf')
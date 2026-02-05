import widgets.config
from widgets.buttons import *
from kivy.app import App
from kivy.lang import Builder
import json

# Carga la interfaz visual definida en main.kv
Builder.load_file("main.kv")

class SuperHeroManager(App):
    """
    Clase principal de la aplicación que hereda de App.
    Se encarga de construir y ejecutar la interfaz gráfica.
    """
    def build(self):
        """
        Método que construye la raíz de la aplicación.
        Retorna:
            Main_Container: El widget principal de la aplicación.
        """
        return Main_Container()
# Inicia la aplicación
SuperHeroManager().run()
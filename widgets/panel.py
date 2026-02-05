from kivy.uix.boxlayout import BoxLayout
from .utils import read_json
import json

class InfoPanel(BoxLayout):
    """
    Panel que muestra información detallada sobre un evento seleccionado.
    Hereda de BoxLayout.
    """
    def __init__(self, size=(400, 500), pos=(350, 100)):
        """
        Inicializa el panel de información.
        Args:
           size: Tamaño inicial del panel.
           pos: Posición inicial del panel.
        """
        super().__init__()
        self.opacity=0
        self.size = size
        def read_json(link):
            with open(link, 'r', encoding='utf-8') as file:
                return json.load(file)
        # Carga la información de los eventos al iniciar
        self.file = read_json("json/info_eventos.json")
    
    def update_info(self, event_id):
        """
        Actualiza los widgets del panel con la información del evento dado.
        Args:
            event_id: El ID del evento a mostrar.
        """
        event_id = str(event_id)
        if event_id in self.file:
            info = self.file[event_id]
            self.ids.title_label.text = info["title"]
            self.ids.desc_label.text = info["description"]
            self.ids.req_label.text = info["requirements"]
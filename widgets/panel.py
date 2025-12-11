from kivy.uix.boxlayout import BoxLayout
from .utils import read_json
import json

class InfoPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity=0
        def read_json(link):
            with open(link, 'r', encoding='utf-8') as file:
                return json.load(file)
        self.file = read_json("json/info_eventos.json")
    
    def update_info(self, event_id):
        event_id = str(event_id)
        if event_id in self.file:
            info = self.file[event_id]
            self.ids.title_label.text = info["title"]
            self.ids.desc_label.text = info["description"]
            self.ids.req_label.text = info["requirements"]
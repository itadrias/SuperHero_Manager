from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from .utils import *
from .checker import *


class AnimatedButton(Button):
    button_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, base_color, target_color, **kwargs):
        super().__init__(**kwargs)
        self.base_color = base_color
        self.target_color = target_color
        self.button_color = base_color
        self.background_normal = ''
        self.glow = None
        self.bind(button_color=self.update_button_color)
        self.start_animation()
    
    def update_button_color(self, *args):
        self.background_color = self.button_color
    
    def start_animation(self):
        anim = Animation(button_color=self.target_color, duration=1.0) + \
               Animation(button_color=self.base_color, duration=1.0)
        anim.repeat = True
        self.glow = anim
        anim.start(self)
    
    def stop_animation(self):
        if self.glow:
            self.glow.cancel(self)
            self.glow = None
        self.button_color = self.base_color

class event_view(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = [50, 20, 50, 50]
        self.add_widget(Label(
            text="Eventos Planificados",
            font_size='50sp',
            font_name='BebasNeue', 
            size_hint_y=None, 
            height=80,
            color=(1, 1, 1, 1)
        ))
        scroll = ScrollView(size_hint=(1, 1))
        self.content = GridLayout(cols=1, spacing=15, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.refresh_list()
        scroll.add_widget(self.content)
        self.add_widget(scroll)
        self.opacity = 0
        self.fading_out = False
        with self.canvas.before:
             Color(0, 0, 0, 0.85)
             self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def refresh_list(self):
        self.content.clear_widgets()
        events = read_json("json/events.json")
        info = read_json("json/info_eventos.json")
        if not events:
            self.content.add_widget(Label(
                text="No hay eventos planificados", 
                font_name='OpenSans', 
                font_size='20sp', 
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=50
            ))
            return
        cont = 0
        for i in events:
            start = events[i]["start"]
            end = events[i]["end"]
            id = str(events[i]["id"])
            resources = events[i]["resources"]
            name = info[id]["title"]
            description = info[id]["description"]
            resource_names = []
            for resource in resources:
                if resource < 17 or resource > 40: 
                    continue
                resource_id = str(resource)
                resource_names.append(info[str(resource)]["title"])
            
            item_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=[20, 10], spacing=20)
            with item_container.canvas.before:
                Color(28/255, 37/255, 48/255, 0.85)
                item_container.rect = RoundedRectangle(pos=item_container.pos, size=item_container.size, radius=[10])
            item_container.bind(pos=self._update_item_rect, size=self._update_item_rect)
            title = Label(
                text=f"[b]{name}[/b]", 
                markup=True,
                font_size='26sp', 
                font_name='BebasNeue', 
                size_hint_x=1,
                halign='left', 
                valign='middle', 
                text_size=(400, None),
                color=(1, 1, 1, 1)
            )
            title.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))
            
            item_container.add_widget(title)

            details = AnimatedButton(
                base_color=(58/255, 80/255, 107/255, 1),
                target_color=(28/255, 50/255, 77/255, 1),
                text="VER DETALLES",
                size_hint=(None, None),
                size=(140, 50),
                pos_hint={'center_y': 0.5},
                font_name='BebasNeue',
                font_size='20sp',
                color=(1,1,1,1)
            )
            details.bind(on_release=lambda instance, t=name, d=description, s=start, e=end, r=resource_names: self.show_details(t, d, s, e, r))
            item_container.add_widget(details)
            delete = AnimatedButton(
                base_color=(139/255, 58/255, 58/255, 1),
                target_color=(109/255, 28/255, 28/255, 1),
                text="ELIMINAR",
                size_hint=(None, None),
                size=(120, 50),
                pos_hint={'center_y': 0.5},
                font_name='BebasNeue',
                font_size='20sp',
                color=(1,1,1,1)
            )
            delete.bind(on_release=lambda instance, k=cont: self.delete_entry(k))
            item_container.add_widget(delete)

            self.content.add_widget(item_container)
            cont += 1

    def _update_item_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def show_details(self, title, description, start, end, resources):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        details_scroll = ScrollView()
        details_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        details_layout.bind(minimum_height=details_layout.setter('height'))

        details_layout.add_widget(Label(
            text="[b]Descripción:[/b]", markup=True, font_name='OpenSans', font_size='18sp', size_hint_y=None, height=30, color=(0.6, 0.8, 1, 1)
        ))
        details_layout.add_widget(Label(
            text=description, 
            font_name='OpenSans', 
            font_size='16sp', 
            size_hint_y=None, 
            text_size=(400, None),
            halign='left'
        ))
        desc_label = details_layout.children[0]
        desc_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        details_layout.add_widget(Label(
            text="[b]Fechas:[/b]", markup=True, font_name='OpenSans', font_size='18sp', size_hint_y=None, height=30, color=(0.6, 0.8, 1, 1)
        ))
        details_layout.add_widget(Label(
            text=f"Inicio: {start}\nFin: {end}", 
            font_name='OpenSans', 
            font_size='16sp', 
            size_hint_y=None, 
            height=50,
            halign='left'
        ))
        details_layout.add_widget(Label(
            text="[b]Recursos Asignados:[/b]", markup=True, font_name='OpenSans', font_size='18sp', size_hint_y=None, height=30, color=(0.6, 0.8, 1, 1)
        ))
        
        res_text = "\n".join([f"• {r}" for r in resources]) if resources else "Ninguno"
        res_label = Label(
            text=res_text, 
            font_name='OpenSans', 
            font_size='16sp', 
            size_hint_y=None, 
            halign='left',
            valign='top'
        )
        res_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        res_label.text_size = (400, None)
        details_layout.add_widget(res_label)

        details_scroll.add_widget(details_layout)
        content.add_widget(details_scroll)

        close = Button(
            text="CERRAR",
            size_hint_y=None,
            height=50,
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp'
        )
        content.add_widget(close)

        popup = Popup(
            title=title,
            title_font='BebasNeue',
            title_size='30sp',
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(500, 600),
            separator_color=(0.17, 0.37, 0.52, 1),
            background_color=(0.1, 0.1, 0.1, 0.95)
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def delete_entry(self, key):
        delete_event(key)
        self.refresh_list()

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def show(self):
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self)

    def fade(self):
        self.fading_out = True
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=self.remove)
        anim.start(self)

    def remove(self, animation, widget):
        if self.parent:
            self.parent.remove_widget(self)

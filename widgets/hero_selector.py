from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import ListProperty
from .sound_manager import *
from .panel import InfoPanel
from kivy.core.window import Window
from .utils import *
from .chart import *

class hero_button(ButtonBehavior, Image):
    border_color = ListProperty([1, 1, 1, 1])
    def __init__(self, id, link):
        super().__init__()
        self.id = id
        self.file = read_json("json/events_parameters.json")
        if(str(self.id) in self.file): self.parameters = self.file[str(self.id)]
        self.source = link
        self.selected = False
        self.size_hint = (None, None)
        self.size = (130, 130)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(border_color=self.update_canvas)
        self.glow = None
        self.sound = SoundManager()
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, window, mouse_pos):
        from .buttons import Main_Container
        if self.disabled:
            return False
        if hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress:
            return False
        if self.collide_point(*mouse_pos):
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, Chart)
            if rec is not None and isinstance(rec.children[index], Chart):
                rec.children[index].hide_chart()
            index = get_index_widget(rec, InfoPanel)
            if rec is not None and isinstance(rec.children[index], InfoPanel):
                self.parent.last = self
                rec.children[index].opacity=1
                rec.children[index].pos=(100, 125)
                rec.children[index].size=(600, 525)
                rec.children[index].update_info(self.id)
        elif self.parent.last==self:
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, InfoPanel)
            if rec is not None and isinstance(rec.children[index], InfoPanel):
                    rec.children[index].opacity=0
            index = get_index_widget(rec, Chart)
            if rec is not None and isinstance(rec.children[index], Chart):
                rec.children[index].show_chart()

    def on_press(self):
        self.selected = not self.selected
        self.sound.play_sound("sounds/hero_click.mp3", 0.1)
        for elements in self.parameters:
            self.parent.sum[elements[0]]+=elements[1] if self.selected else -elements[1]
        if self.selected:
            self.start()
        else:
            self.stop()
        from .buttons import Main_Container
        rec = look_for_master(self, Main_Container)
        index = get_index_widget(rec, Chart)
        if rec is not None and isinstance(rec.children[index], Chart):
            parameters = []
            for i in range(6):
                parameters.append((i, min(10, self.parent.sum[i])))
            rec.children[index].draw_chart_over(parameters)
        self.update_canvas()

    def start(self):
        self.border_color = [204/255, 85/255, 0, 1]
        anim = Animation(border_color=[1, 0.9, 0.5, 1], duration=0.5) + \
               Animation(border_color=[204/255, 85/255, 0, 1], duration=0.5)
        anim.repeat = True
        self.glow = anim
        anim.start(self)

    def stop(self):
        if self.glow:
            self.glow.cancel(self)
            self.glow = None
        self.border_color = [1, 1, 1, 1]

    def update_canvas(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(*self.border_color)
            width = 2 if self.selected else 1
            Line(rectangle=(self.x, self.y, self.width, self.height), width=width)

class scroll_matrix(GridLayout):
    def __init__(self):
        super().__init__()
        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}
        self.cols = 3
        self.spacing = 5
        self.padding = 25
        self.last = None
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.sum = [0, 0, 0, 0, 0, 0]

        for i in range(12):
            btn = hero_button(id=i+17, link=f'images/heroes/hero_{i+1}.jpg')
            self.add_widget(btn)

class hero_matrix(FloatLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(Label(text="Selecciona tu héroe", font_name='BebasNeue', font_size='40sp', pos=(975, 550), size_hint=(None, None)))
        self.size_hint = (None, None)
        self.size = (450, 650)
        self.pos =  (800, 0)
        self.add_widget(scroll_matrix())
        self.opacity = 0
        self.animation_in_progress = False
        self.buttons_disabled = False

    def show(self):
        self.animation_in_progress = True
        self.buttons_disabled = True
        animation = Animation(opacity=1, duration=0.5, t='out_quad')
        def enable(animation, widget):
            self.animation_in_progress = False
            self.buttons_disabled = False
        animation.bind(on_complete=enable)
        animation.start(self)
    
    def fade(self):
        if self.animation_in_progress:
            return
        self.animation_in_progress = True
        self.buttons_disabled = True
        
        animation = Animation(opacity=0, duration=0.2, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)
    
    def remove(self, animation, widget):
        if self.parent:
            self.parent.remove_widget(self)
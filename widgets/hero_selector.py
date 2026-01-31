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

sum = [0, 0, 0, 0, 0, 0]
used = {}

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
        try:
            self.selected = used[self.id]
        except:
            used[self.id] = False
        if self.selected:
            self.start()
        else:    
            self.stop()

    def on_touch_down(self, touch):
        if self.disabled: return False
        
        if touch.button == 'left':
            return super().on_touch_down(touch)
        
        if touch.button == 'right':
            if self.collide_point(*touch.pos):
                touch.grab(self)
                self.display_info(True)
                return True
        return False

    def on_touch_up(self, touch):
        if touch.button == 'right' and touch.grab_current is self:
            touch.ungrab(self)
            self.display_info(False)
            return True
        return super().on_touch_up(touch)
    
    def display_info(self, show):
        from .buttons import Main_Container
        if self.disabled:
            return
        if hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress:
            return
        rec = look_for_master(self, Main_Container)
        if not rec: return
        if show:
            index = get_index_widget(rec, Chart)
            if index != -1 and isinstance(rec.children[index], Chart):
                rec.children[index].hide_chart()
            index = get_index_widget(rec, InfoPanel)
            if index != -1 and isinstance(rec.children[index], InfoPanel):
                self.parent.last = self
                rec.children[index].opacity=1
                rec.children[index].pos=(100, 125)
                rec.children[index].size=(600, 525)
                rec.children[index].update_info(self.id)
        else:
            index = get_index_widget(rec, InfoPanel)
            if index != -1 and isinstance(rec.children[index], InfoPanel):
                    rec.children[index].opacity=0
            index = get_index_widget(rec, Chart)
            if index != -1 and isinstance(rec.children[index], Chart):
                rec.children[index].show_chart()

    def on_press(self):
        self.selected = not self.selected
        used[self.id] = self.selected
        self.sound.play_sound("sounds/hero_click.mp3", 0.1)
        for elements in self.parameters:
            sum[elements[0]]+=elements[1] if self.selected else -elements[1]
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
                parameters.append((i, min(10, sum[i])))
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

class hero_matrix(GridLayout):
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

        for i in range(12):
            btn = hero_button(id=i+17, link=f'images/heroes/hero_{i+1}.jpg')
            self.add_widget(btn)

class item_matrix(GridLayout):
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
        for i in range(12):
            btn = hero_button(id=i+29, link=f'images/items/item_{i+1}.png')
            self.add_widget(btn)

class selection_matrix(FloatLayout):
    def __init__(self, mode=1):
        super().__init__()
        if mode == 1:
            self.add_widget(Label(text="Selecciona tus héroes", font_name='BebasNeue', font_size='40sp', pos=(975, 550), size_hint=(None, None)))
        else:
            self.add_widget(Label(text="Selecciona tus ítems", font_name='BebasNeue', font_size='40sp', pos=(975, 550), size_hint=(None, None)))
        self.size_hint = (None, None)
        self.size = (450, 650)
        self.pos =  (800, 0)
        if mode == 1:
            self.add_widget(hero_matrix())
        else:
            self.add_widget(item_matrix())
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
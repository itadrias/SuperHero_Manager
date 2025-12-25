from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from .utils import *
from .panel import *
from .chart import *
from .sound_manager import *
from .hero_selector import *

record = []

class Main_Container(FloatLayout):
    def __init__(self):
        super().__init__()
        self.background = Image(source="images/main_background_1.jpg")
        self.add_widget(self.background)
        
        child = main_button_container(100, "0", (100, 100))
        self.add_widget(InfoPanel())
        self.add_widget(child)
        child.show()
        
        self.sound = SoundManager()
        child = sound_button(-1, "images/sound.png")
        self.add_widget(child)
        child.show((1280, 25))
        self.sound.play_sound("sounds/main_theme.mp3", 0.7, 1)
    
    def swap_backgrounds(self, link):
        background = Image(source=link, size=(1280, 680))
        background.opacity = 0
        self.add_widget(background, index=20)
        first = Animation(opacity=0, duration=0.3)
        second = Animation(opacity=1, duration=0.3)
        first.start(self.background)
        second.start(background)
        
        def remove(animation, widget):
            self.remove_widget(self.background)
            self.background = background
        
        first.bind(on_complete=remove)

class main_button_container(BoxLayout):
    def __init__(self, move, events, positions):
        super().__init__()
        self.animation_in_progress = False
        self.move = move
        self.pos = positions
        self.buttons = read_json("json/options.json")
        for elements in self.buttons[events]:
            self.add_widget(change_button(*elements))
        self.opacity = 0
        self.x -= self.move
        self.last = None
        record.append(self)
    
    def buttons_disabled(self, disabled):
        for child in self.children:
            if isinstance(child, change_button):
                child.disabled = disabled
    
    def show(self):
        self.animation_in_progress = True
        self.buttons_disabled(True)
        animation = Animation(x=self.x+self.move, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        self.animation_in_progress = False
        self.buttons_disabled(False)
    
    def fade(self):
        if look_for_child(self.parent, volver_button) is None:
            self.parent.add_widget(volver_button(0, "images/volver.jpg"))
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.buttons_disabled(True)
        
        animation = Animation(x=self.x-self.move, opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=self.remove)
        
        rec = look_for_master(self, Main_Container)
        if rec:
            index = get_index_widget(rec, InfoPanel)
            if index < len(rec.children) and isinstance(rec.children[index], InfoPanel):
                rec.children[index].opacity = 0
        animation.start(self)
    
    def remove(self, animation, widget):
        if self.parent:
            self.parent.remove_widget(self)

class sound_button(ButtonBehavior, Image):
    def __init__(self, id, link):
        super().__init__()
        self.source = link
        self.id = id
        self.sound = SoundManager()
        self.animation_in_progress = False
    
    def show(self, coords):
        self.pos = coords
        coming_from = -100
        if self.x == 1280:
            coming_from = 100
        self.y-=coming_from
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y+coming_from, opacity=1, duration=0.2, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        self.animation_in_progress = False
        self.disabled = False
    
    def fade(self):
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.disabled = True
        coming_from = -100
        if self.x == 1110:
            coming_from = 100
        animation = Animation(y=self.y-coming_from, opacity=0, duration=0.2, t='out_quad')
        animation.bind(on_complete=self.remove)
        
        rec = look_for_master(self, Main_Container)
        if rec:
            index = get_index_widget(rec, InfoPanel)
            if index < len(rec.children) and isinstance(rec.children[index], InfoPanel):
                rec.children[index].opacity = 0
        animation.start(self)
    
    def remove(self, animation, widget):
        if self.parent:
            self.parent.remove_widget(self)

    def on_touch_down(self, touch):
        if self.disabled or (hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress):
            return False
        if self.collide_point(*touch.pos):
            main = look_for_master(self, Main_Container)
            if main.sound.sound.volume != 0:
                main.sound.sound.volume = 0
                self.source = "images/mute.png"
            else:
                main.sound.sound.volume = 0.7
                self.source = "images/sound.png"
    


class change_button(ButtonBehavior, Image):
    def __init__(self, id, link):
        super().__init__()
        self.source = link
        self.size_hint=(None, None)
        self.size=(200, 100)
        self.id = id
        self.is_hovered = False
        self.file = read_json("json/events_parameters.json")
        if(str(self.id) in self.file): self.parameters = self.file[str(self.id)]
        self.sound = SoundManager()
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, window, mouse_pos):
        if self.disabled:
            return False
        if hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress:
            return False
        if self.collide_point(*mouse_pos):
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, InfoPanel)
            if rec is not None and isinstance(rec.children[index], InfoPanel):
                self.parent.last = self
                rec.children[index].opacity=1
                rec.children[index].update_info(self.id)
        elif self.parent.last==self:
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, InfoPanel)
            if rec is not None and isinstance(rec.children[index], InfoPanel):
                    rec.children[index].opacity=0
    
    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress:
            return False
            
        if self.collide_point(*touch.pos):
            self.parent.fade()
            self.sound.play_sound("sounds/click.mp3")
            rec = look_for_master(self, Main_Container)
            sound = look_for_child(rec, sound_button)
            if self.id <= 4:
                sound.fade()
                link = "images/sound.png"
                if rec.sound.sound.volume == 0: 
                    link = "images/mute.png"
                child = sound_button(-1, link)
                rec.add_widget(child)
                child.show((20, 600))
            elif self.id <= 12 and self.id%4:
                child = Chart()
                child.draw(self.parameters)
                rec.add_widget(child)
                record.append(child)
                child = hero_matrix()
                child.show()
                rec.add_widget(child)
            elif self.id >= 13:
                child = Chart(self.id == 16)
                child.draw(self.parameters)
                rec.add_widget(child)
                record.append(child)
            if self.id == 1:
                child = main_button_container(-100, "1", (1050, 100))
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_2.jpg")
                child.show()
            if self.id == 2:
                child = main_button_container(-100, "3", (1050, 100))
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_3.jpeg")
                child.show()
            if self.id == 8:
                record.pop()
                child = main_button_container(-100, "2", (1050, 100))
                self.parent.parent.add_widget(child)
                child.show()
            if self.id == 12:
                record.pop()
                child = main_button_container(-100, "1", (1050, 100))
                self.parent.parent.add_widget(child)
                child.show()
            return True
        return super().on_touch_down(touch)

class volver_button(ButtonBehavior, Image):
    def __init__(self, id, link):
        super().__init__()
        self.animation_in_progress = False
        self.disabled = False
        self.source = link
        self.y -= 100
        self.sound = SoundManager()
        self.show()
    
    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if self.collide_point(*touch.pos):
            record.pop()
            child = record[-1]
            if len(record) == 1:
                self.fade()
            self.sound.play_sound("sounds/click.mp3")
            for element in self.parent.children:
                if element == self or isinstance(element, sound_button):
                    continue
                try:
                    element.fade()
                except:
                    pass
            
            rec = look_for_master(self, Main_Container)
            try:
                rec.add_widget(child)
                child.show()
            except Exception:
                pass
            
            if len(record) == 1:
                look_for_child(rec, sound_button).fade()
                link = "images/mute.png" if rec.sound.sound.volume == 0 else "images/sound.png"
                child = sound_button(-1, link)
                self.parent.add_widget(child)
                child.show((1280, 25))
                self.parent.swap_backgrounds("images/main_background_1.jpg")
            
            self.disabled = True
            animation = Animation(duration=0.5)
            animation.bind(on_complete=lambda a, w: setattr(self, 'disabled', False))
            animation.start(self)
            return True
        return super().on_touch_down(touch)

    def show(self):
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y+100, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        self.animation_in_progress = False
        self.disabled = False

    def fade(self):
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y-100, opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)

    def remove(self, animation, widget):
        if self.parent:
            self.parent.remove_widget(self)
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from .utils import *
from .panel import *
from .chart import *
from .sound_manager import *
from .hero_selector import *
from .restrictions import *
from .date_selector import *
from .add import *
from .events_view import *

record = []

class Main_Container(FloatLayout):
    """
    Contenedor principal de la aplicación.
    Gestiona la navegación entre menús y el fondo animado.
    """
    def __init__(self):
        super().__init__()
        self.background = Image(source="images/main_background_1.jpg")
        self.add_widget(self.background)
        
        # Inicializa el menú principal
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
        """
        Cambia el fondo de la aplicación con una animación de fundido (fade).
        Args:
            link: Ruta de la nueva imagen de fondo.
        """
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
    """
    Contenedor para los botones de navegación.
    Maneja las animaciones de entrada y salida de los menús.
    """
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
        """
        Activa o desactiva todos los botones contenidos en este contenedor.
        Args:
            disabled (bool): True para desactivar, False para activar.
        """
        for child in self.children:
            if isinstance(child, change_button):
                child.disabled = disabled
    
    def show(self):
        """Anima la entrada del contenedor de botones."""
        self.animation_in_progress = True
        self.buttons_disabled(True)
        animation = Animation(x=self.x+self.move, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        """
        Callback que se ejecuta al terminar la animación de entrada.
        Rehabilita la interacción con los botones.
        """
        self.animation_in_progress = False
        self.buttons_disabled(False)
    
    def fade(self):
        """Anima la salida del contenedor de botones y muestra el botón 'volver'."""
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
    """
    Botón que controla el encendido y apagado del sonido global de la aplicación.
    """
    def __init__(self, id, link):
        """
        Inicializa el botón de sonido.
        Args:
            id: Identificador del botón.
            link: Ruta de la imagen del ícono (activado/desactivado).
        """
        super().__init__()
        self.source = link
        self.id = id
        self.sound = SoundManager()
        self.animation_in_progress = False
    
    def show(self, coords):
        """
        Anima la entrada del botón de sonido.
        Args:
            coords: Tupla (x, y) con la posición final.
        """
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
        """Habilita el botón tras la animación."""
        self.animation_in_progress = False
        self.disabled = False
    
    def fade(self):
        """Oculta el botón con animación."""
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.disabled = True
        coming_from = -100
        if self.x == 1280:
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
        """Elimina el widget del padre."""
        if self.parent:
            self.parent.remove_widget(self)

    def on_touch_down(self, touch):
        """Maneja el clic para activar/desactivar sonido."""
        if touch.button != 'left': return False
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
        self.events_name = read_json("json/info_eventos.json")
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
                if self.id <= 4:
                    rec.children[index].pos=(475, 100)
                    rec.children[index].size=(400, 500)
                else:
                    rec.children[index].pos=(475, 100)
                    rec.children[index].size=(400, 500)
                rec.children[index].update_info(self.id)
        elif self.parent.last==self:
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, InfoPanel)
            if rec is not None and isinstance(rec.children[index], InfoPanel):
                    rec.children[index].opacity=0
    
    def on_touch_down(self, touch):
        if touch.button != 'left': return super().on_touch_down(touch)
        if self.disabled:
            return False
        if hasattr(self.parent, 'animation_in_progress') and self.parent.animation_in_progress:
            return False
            
        if self.collide_point(*touch.pos):
            self.parent.fade()
            self.sound.play_sound("sounds/click.mp3")
            rec = look_for_master(self, Main_Container)
            rec.mission = self.id
            sound = look_for_child(rec, sound_button)
            if self.id <= 4:
                sound.fade()
                link = "images/sound.png"
                if rec.sound.sound.volume == 0: 
                    link = "images/mute.png"
                child = sound_button(-1, link)
                rec.add_widget(child)
                child.show((20, 600))
            elif (self.id <= 12 and self.id%4) or self.id >= 13:
                child = Chart(self.id == 16, 0, self.events_name[str(self.id)]["title"])
                child.draw(self.parameters)
                rec.add_widget(child)
                record.append(child)
                child = selection_matrix(1, True)
                child.show()
                rec.add_widget(child)
                child = bottom_button("images/siguiente.jpg", rec)
                rec.add_widget(child)
            if self.id == 1:
                child = main_button_container(-100, "1", (1050, 100))
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_2.png")
                child.show()
            if self.id == 2:
                child = main_button_container(-100, "3", (1050, 100))
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_3.jpeg")
                child.show()
            if self.id == 3:
                self.events_name = read_json("json/info_eventos.json")
                def on_name_entered(name):
                    if name.strip():
                        child = Chart(self.id == 16, 0, name)
                        rec.add_widget(child)
                        record.append(child)
                        child = selection_matrix(1, True)
                        child.show()
                        rec.add_widget(child)
                        founded = False
                        cont = 0
                        for i in self.events_name:
                            if name == self.events_name[str(i)]["title"]:
                                rec.mission = cont
                                founded = True
                            cont += 1
                        if not founded:
                            rec.mission = len(self.events_name)
                            self.events_name[rec.mission] ={
                                "title": name,
                                "description": "Evento personalizado.",
                                "requirements": ""
                            }
                            write_json("json/info_eventos.json", self.events_name)
                    else:
                        for child in [child for child in rec.children]:
                            if isinstance(child, (bottom_button, next_bottom_button, sound_button)):
                                rec.remove_widget(child)
                        
                        record.clear()
                        child = sound_button(-1, "images/sound.png")
                        rec.add_widget(child)
                        child.show((1280, 25))
                        child = main_button_container(100, "0", (100, 100))
                        rec.add_widget(child)
                        rec.swap_backgrounds("images/main_background_1.jpg")
                        child.show()
                        btn = look_for_child(rec, volver_button)
                        if btn:
                            rec.remove_widget(btn)
                
                child = enter_name(callback=on_name_entered)
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_3.jpeg")
                child = bottom_button("images/siguiente.jpg", rec)
                rec.add_widget(child)
            if self.id == 4:
                child = event_view()
                rec.add_widget(child)
                rec.swap_backgrounds("images/main_background_2.png")
                child.show()
                record.append(child)
                btn = look_for_child(rec, volver_button)
                if btn:
                    rec.remove_widget(btn)
                    rec.add_widget(btn)

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
    """
    Botón para regresar al menú anterior.
    """
    def __init__(self, id, link):
        """
        Inicializa el botón.
        Args:
            id: Identificador.
            link: Ruta de la imagen.
        """
        super().__init__()
        self.animation_in_progress = False
        self.disabled = False
        self.source = link
        self.y -= 100
        self.sound = SoundManager()
        self.show()
    
    def on_touch_down(self, touch):
        """
        Maneja el clic para volver atrás.
        """
        if touch.button != 'left': return super().on_touch_down(touch)
        if self.disabled:
            return 
        rec = look_for_master(self, Main_Container)
        for child in rec.children:
            try:
                if child.disabled:
                    return False
            except:
                pass
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
        """Muestra el botón."""
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y+100, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        """Habilita el botón."""
        self.animation_in_progress = False
        self.disabled = False

    def fade(self):
        """Oculta el botón."""
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y-100, opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)

    def remove(self, animation, widget):
        """Elimina el botón."""
        if self.parent:
            self.parent.remove_widget(self)

class bottom_button(ButtonBehavior, Image):
    """
    Botón siguiente/atrás para navegar entre listas (héroes/items).
    """
    def __init__(self, link, rec):
        """
        Inicializa el botón.
        Args:
           link: Imagen.
           rec: Referencia al contenedor principal.
        """
        super().__init__()
        self.rec = rec
        self.animation_in_progress = False
        self.disabled = False
        self.source = link
        self.sound = SoundManager()
        child = next_bottom_button("images/ayuda.png")
        self.rec.add_widget(child)
        self.brother = child
        self.show()
    
    def on_touch_down(self, touch):
        """Maneja el clic para cambiar de lista."""
        if touch.button != 'left': return super().on_touch_down(touch)
        if self.disabled:
            return False
        if self.collide_point(*touch.pos):
            self.sound.play_sound("sounds/click.mp3")
            rec = look_for_master(self, Main_Container)
            index = get_index_widget(rec, selection_matrix)
            try:
                rec.children[index].fade()
            except Exception:
                pass
            self.disabled = True
            animation = Animation(duration=0.5)
            animation.bind(on_complete=lambda a, w: setattr(self, 'disabled', False))
            animation.start(self)
            self.brother.change()
            self.change()
            return True
        return super().on_touch_down(touch)
    
    def change(self):
        """Cambia el estado del botón (siguiente <-> atras)."""
        animation = Animation(opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        rec = look_for_master(self, Main_Container)
        animation.start(self)
        if self.source == "images/siguiente.jpg": 
            self.source = "images/atras.jpg"
            child = selection_matrix(2)
        else: 
            self.source = "images/siguiente.jpg"
            child = selection_matrix(1)
        child.show()
        rec.add_widget(child)
        animation = Animation(opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)

    def show(self):
        """Muestra el botón."""
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y+100, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        """Habilita el botón."""
        self.animation_in_progress = False
        self.disabled = False

    def fade(self):
        """Oculta el botón."""
        if self.animation_in_progress:
            return
        self.brother.fade()
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y-100, opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)

    def remove(self, animation, widget):
        """Elimina el botón."""
        if self.parent:
            self.parent.remove_widget(self)

class next_bottom_button(ButtonBehavior, Image):
    """
    Botón de acción secundaria (Ayuda / Aceptar misión).
    """
    def __init__(self, link):
        """
        Inicializa el botón.
        Args:
           link: Ruta de la imagen.
        """
        super().__init__()
        self.animation_in_progress = False
        self.disabled = False
        self.source = link
        self.sound = SoundManager()
        self.show()
    
    def finished(self):
        """Bloquea el botón temporalmente."""
        self.disabled = True
        animation = Animation(duration=0.5)
        animation.bind(on_complete=lambda a, w: setattr(self, 'disabled', False))
        animation.start(self)
        return True
    
    def on_touch_down(self, touch):
        """Maneja el clic (Ayuda o Confirmación)."""
        if touch.button != 'left': return super().on_touch_down(touch)
        if self.disabled:
            return False
        if self.collide_point(*touch.pos):
            self.sound.play_sound("sounds/click.mp3")
            if self.source == "images/ayuda.png":
                layout = BoxLayout(orientation='vertical', spacing=15, padding=25)
                info_label = Label(
                    text='Para cumplir la misión, debes seleccionar un equipo y equiparlos, cubriendo los requisitos mínimos (polígono blanco) en el gráfico.\n\n[color=8B3A3A]RESTRICCIONES Y REGLAS:[/color]\n- Algunos héroes [b]no pueden ir juntos[/b] o requieren un [b]compañero específico[/b].\n- Ciertas misiones exigen [b]items obligatorios[/b].\n- Mínimo requieres [b]1 héroe[/b] y [b]1 item[/b].\n\n[i][color=aaaaaa]Tip: Mantén presionado Click Derecho sobre héroes o items para ver sus detalles.[/color][/i]',
                    halign='center',
                    valign='middle',
                    font_name='OpenSans',
                    font_size='16sp',
                    markup=True,
                    color=(0.9, 0.9, 0.9, 1)
                )
                info_label.bind(size=info_label.setter('text_size'))
                layout.add_widget(info_label)
                close = Button(
                    text='ENTENDIDO',
                    size_hint=(1, None),
                    height=60,
                    background_normal='',
                    background_color=(0.17, 0.37, 0.52, 1),
                    font_name='BebasNeue',
                    font_size='26sp',
                    color=(1, 1, 1, 1)
                )
                layout.add_widget(close)
                popup = Popup(
                    title='INFORMACIÓN DE MISIÓN',
                    title_font='BebasNeue',
                    title_size='32sp',
                    title_align='center',
                    content=layout,
                    size_hint=(None, None),
                    size=(720, 600),
                    auto_dismiss=False,
                    title_color = (0.17, 0.37, 0.52, 1),
                    separator_color=(0.17, 0.37, 0.52, 1),
                    background_color=(0.1, 0.1, 0.1, 0.95),
                    overlay_color=(0, 0, 0, 0.7)
                )
                close.bind(on_press=popup.dismiss)
                popup.open()
            else:
                ids = [k for k, v in used.items() if v]
                rec = look_for_master(self, Main_Container)
                if hasattr(rec, 'mission'):
                    ids.append(rec.mission)
                valid, msg = check_restrictions(ids, sum)
                if not valid:
                    popup = Popup(
                        title='RESTRICCIÓN',
                        title_font='BebasNeue',
                        title_size='30sp',
                        title_align='center',
                        content=Label(text=msg, text_size=(380, None), halign='center', valign='middle', font_name='OpenSans'),
                        size_hint=(None, None),
                        size=(420, 250),
                        separator_color=(0.8, 0.2, 0.2, 1),
                        background_color=(0.1, 0.1, 0.1, 0.95),
                        overlay_color=(0, 0, 0, 0.7)
                    )
                    popup.open()
                    return True
                date_selector(self.finished(), ids).open()
            return True
        return super().on_touch_down(touch)
    
    def change(self):
        """Alterna entre Ayuda y Aceptar."""
        animation = Animation(opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
        if self.source == "images/aceptar.png": 
            self.source = "images/ayuda.png"
        else: 
            self.source = "images/aceptar.png"
        animation = Animation(opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)

    def show(self):
        """Muestra el botón."""
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y+100, opacity=1, duration=0.5, t='out_quad')
        animation.bind(on_complete=lambda a, w: self._enable(a, w))
        animation.start(self)
    
    def _enable(self, animation, widget):
        """Habilita el botón."""
        self.animation_in_progress = False
        self.disabled = False

    def fade(self):
        """Oculta el botón."""
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.disabled = True
        animation = Animation(y=self.y-100, opacity=0, duration=0.5, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)

    def remove(self, animation, widget):
        """Elimina el botón."""
        if self.parent:
            self.parent.remove_widget(self)
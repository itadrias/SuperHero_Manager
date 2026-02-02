from os import remove
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from datetime import datetime
from .checker import *

class date_box(BoxLayout):
    def __init__(self, text, date):
        super().__init__()
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 80

        self.add_widget(Label(
            text=text, 
            font_name='BebasNeue', 
            font_size='24sp', 
            size_hint_y=None, 
            height=30,
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
            text_size=(400, None)
        ))
        controls = BoxLayout(spacing=5)

        days = [str(n).zfill(2) for n in range(1, 32)]
        months = [str(n).zfill(2) for n in range(1, 13)]
        years = [str(n) for n in range(date.year, date.year + 100)]
        hours = [str(n).zfill(2) for n in range(24)]
        minutes = [str(n).zfill(2) for n in range(0, 60, 5)]

        self.day = self.spinner(days, str(date.day).zfill(2))
        self.month = self.spinner(months, str(date.month).zfill(2))
        self.year = self.spinner(years, str(date.year))
        self.hour = self.spinner(hours, str(date.hour).zfill(2))
        self.minute = self.spinner(minutes, str(date.minute//5*5).zfill(2))

        controls.add_widget(self.day)
        controls.add_widget(self.month)
        controls.add_widget(self.year)
        controls.add_widget(Label(text='-', size_hint_x=None, width=10))
        controls.add_widget(self.hour)
        controls.add_widget(Label(text=':', size_hint_x=None, width=5))
        controls.add_widget(self.minute)

        self.add_widget(controls)

    def spinner(self, values, default):
        s = Spinner(
            text=default,
            values=values,
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_name='OpenSans',
            size_hint_y=None,
            height=40
        )
        return s
        
    def validate_day(self):
        try:
            s = f"{self.year.text}-{self.month.text}-{self.day.text} {self.hour.text}:{self.minute.text}"
            return datetime.strptime(s, "%Y-%m-%d %H:%M")
        except ValueError:
            return None

class date_selector(Popup):
    def __init__(self, finished, ids):
        super().__init__()
        self.resources = sorted(ids)
        self.finished = finished
        self.title = 'SELECCIONAR FECHAS'
        self.title_font = 'BebasNeue'
        self.title_size = '32sp'
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (600, 480)
        self.separator_color = (0.17, 0.37, 0.52, 1)
        self.background_color = (0.1, 0.1, 0.1, 0.95)
        self.overlay_color = (0, 0, 0, 0.7)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=25)
        self.error = Label(
            text='', 
            color=(0.17, 0.37, 0.52, 1), 
            size_hint_y=None, 
            height=30,
            font_name='BebasNeue',
            font_size=30,
            markup=True
        )

        self.start = date_box("INICIO", datetime.now())
        self.end = date_box("FIN", datetime.now())

        layout.add_widget(self.error)
        layout.add_widget(self.start)
        layout.add_widget(self.end)
        selection = BoxLayout(size_hint_y=None, height=60, spacing=20)
        selection.add_widget(Button(
            text='SALIR',
            background_normal='',
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp',
            on_press=self.dismiss
        ))
        selection.add_widget(Button(
            text='BUSCAR HUECO',
            background_normal='',
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp',
            on_press=self.finding
        ))
        selection.add_widget(Button(
            text='CONFIRMAR',
            background_normal='',
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp',
            on_press=self.create
        ))
        layout.add_widget(selection)
        self.layout = layout
        self.selection = selection
        self.content = layout

    def validate(self, *args):
        start = self.start.validate_day()
        end = self.end.validate_day()

        if not start or not end:
            self.error.text = "El mes seleccionado no tiene tantos días"
            return False
        if start >= end:
            self.error.text = "El inicio debe ser anterior al fin"
            return False
        return True

    def finding(self, instance):
        if not self.validate():
            return
        self.error.text=""
        start = self.start.validate_day()
        end = self.end.validate_day()
        overlap = check_overlapping(start, end, self.resources)
        if not overlap:
            self.error.text = f"No existe conflicto de horario" 
            return
        remove = []
        for child in self.layout.children:
            remove.append(child)
        for i in remove:
            self.layout.remove_widget(i)
        start, end = next_available(start, end, self.resources)
        self.start = date_box("INICIO", start)
        self.end = date_box("FIN", end)
        self.layout.add_widget(self.error)
        self.layout.add_widget(self.start)
        self.layout.add_widget(self.end)
        self.layout.add_widget(self.selection)
        self.error.text = f"Actualizado a la próxima fecha más cercana" 
        return
    
    def create(self, instance):
        if not self.validate():
            return
        self.error.text=""
        start = self.start.validate_day()
        end = self.end.validate_day()
        overlap = check_overlapping(start, end, self.resources)
        if overlap:
            self.error.text = f"Conflicto de horario (Ocupado hasta {overlap})" 
            return
        self.error.text = f"Evento creado exitosamente" 
        create_event(start, end, self.resources[0], self.resources)
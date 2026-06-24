from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class enter_name(BoxLayout):
    """
    Popup personalizado para ingresar el nombre de un evento personalizado.
    Hereda de BoxLayout.
    """
    def __init__(self, callback=None):
        """
        Inicializa el widget y muestra el popup.
        Args:
            callback: Función a llamar con el nombre ingresado al aceptar.
        """
        super().__init__()
        self.callback = callback
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        layout.add_widget(Label(
            text='Ingrese el Nombre del Evento:',
            font_size=25,
            font_name='OpenSans',
        )) 
        self.name = TextInput(
            multiline=False,
            size_hint=(1, None),
            height=50,
            font_name = 'OpenSans',
            font_size = '20sp'
        )
        popup = Popup(
            title='Evento Personalizado',
            title_font = 'BebasNeue',
            title_align = 'center',
            title_size = '25sp',
            content=layout,
            size_hint=(None, None),
            size=(500, 300),
            separator_color = (0.17, 0.37, 0.52, 1),
            background_color = (0.1, 0.1, 0.1, 0.95),
            auto_dismiss=False
        )
        self.popup = popup
        layout.add_widget(self.name)
        rec = BoxLayout(spacing=10)
        # Botones de Cancelar y Aceptar
        rec.add_widget(Button(
            text='CANCELAR',
            background_normal='',
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp',
            on_press=self.cancel
        ))
        rec.add_widget(Button(
            text='ACEPTAR',
            background_normal='',
            background_color=(0.17, 0.37, 0.52, 1),
            font_name='BebasNeue',
            font_size='24sp',
            on_press=self.to_accept
        ))
        layout.add_widget(rec)
        popup.open()

    def cancel(self, instance):
        """Cierra el popup sin realizar acción."""
        self.name.text = ""
        self.popup.dismiss()
        if self.parent:
            self.parent.remove_widget(self)
        if self.callback:
            self.callback("")

    def to_accept(self, instance):
        """Valida la entrada y llama al callback con el nombre."""
        name = self.name.text
        if name.strip() and len(name) <= 30:
            self.popup.dismiss()
            if self.parent:
                self.parent.remove_widget(self)
            if self.callback:
                self.callback(name)
from kivy.core.audio import SoundLoader

class SoundManager:
    """
    Clase encargada de gestionar la carga y reproducción de sonidos.
    """
    def __init__(self):
        super().__init__()
        self.sound = ""

    def play_sound(self, link, volume=1.0, loop=False):
        """
        Reproduce un archivo de sonido.
        Args:
            link: La ruta del archivo de sonido.
            volume: El volumen de reproducción (0.0 a 1.0).
            loop: Booleano para indicar si el sonido debe repetirse en bucle.
        """
        self.sound = SoundLoader.load(link)
        self.sound.play()
        self.sound.volume=volume
        self.sound.loop=loop
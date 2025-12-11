from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        super().__init__()
        self.sound = ""

    def play_sound(self, link, volume, loop):
        self.sound = SoundLoader.load(link)
        self.sound.play()
        self.sound.volume=volume
        self.sound.loop=loop
from kivy.graphics import Color, Line, Triangle, InstructionGroup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from math import cos, sin, pi
from random import randrange

def calculate_position_of_chart(id, value, centerx=325, centery=400, rad=200, cant=10):
    if id <=2:
        y= abs(rad*sin((30+60*id)*(pi/180)))/cant*value+centery
    else:
        y= centery - abs(rad*sin((30+60*id)*(pi/180)))/cant*value
    if id == 0 or id>=4:
        x = abs(rad*cos((30+60*id)*(pi/180)))/cant*value+centerx
    else:
        x = centerx - abs(rad*cos((30+60*id)*(pi/180)))/cant*value
    return (x, y)

class Name(Label):
    def __init__(self, text, pos):
        super().__init__()
        self.text=text
        self.size_hint= (None, None)
        self.pos = pos
        self.height=40
        self.font_size='35sp'
        self.color=(1, 1, 1, 1)
        self.font_name = 'BebasNeue'

class Chart(FloatLayout):
    def __init__(self, special = False, anim = 0):
        super().__init__()
        self.special = special
        self.event = None
        self.opacity = 0
        self.dynamic = InstructionGroup()
        coords=[(325, 600), (498.21, 500), (498.21, 300), (325, 200), (151.80, 300), (151.80, 500)]
        with self.canvas:
            Color(1, 1, 1, 1)
            for j in range(6):
                for i in range(len(coords)):
                    new_points = []
                    for k in range(len(coords)):
                        new_points.append(calculate_position_of_chart(k, j, cant=5))
                    Line(points=[*new_points[i], *new_points[(i+1)%len(new_points)]], width=1)
            for i in range(len(coords)):
                Line(points=[*coords[i], 325, 400], width=1)
            Color(0, 0, 0, 0.65)
            for i in range(6): Triangle(points=[*new_points[i], *new_points[(i+1)%6], 325, 400])
        self.canvas.add(self.dynamic)
        for x, y in [("Inteligencia", (275, 615)), ("Fuerza", (515, 500)), ("Resistencia", (545, 250)),
                     ("Movilidad", (275, 140)), ("Carisma", (35, 250)), ("Sigilo", (35, 500))]:
            self.add_widget(Name(x, y))
        Animation(opacity=1, duration=1, t='out_quad').start(self)

    def fade(self):
        animation = Animation(y=self.y-100, opacity=0, duration=0.2, t='out_quad')
        animation.bind(on_complete=self.remove)
        animation.start(self)

    def remove(self, animation, widget):
        if self.event:
            self.event.cancel()
        if self.parent:
            self.parent.remove_widget(self)
    
    def draw(self, parameters):
        self.parameters = parameters
        if self.special:
            self.update_chart(0)
            self.event = Clock.schedule_interval(self.update_chart, 0.2)
        else:
            self.draw_chart(self.parameters)

    def update_chart(self, dt):
        new_params = []
        for i in range(len(self.parameters)):
             new_params.append([i, randrange(0, 10)])
        self.draw_chart(new_params)

    def draw_chart(self, parameters):
        self.dynamic.clear()
        self.dynamic.add(Color(1, 1, 1, 0.5))
        pointss = []
        for i in parameters:
            pointss.append(calculate_position_of_chart(*i))
        for i in range(len(pointss)):
            self.dynamic.add(Triangle(points=[*pointss[i], *pointss[(i+1)%len(pointss)], 325, 400]))
        self.dynamic.add(Color(1, 1, 1, 1))
        for i in range(len(pointss)):
            self.dynamic.add(Line(points=[*pointss[i], *pointss[(i+1)%len(pointss)]], width=3))
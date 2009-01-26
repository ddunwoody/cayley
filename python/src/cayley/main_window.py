from pyglet.gl import *
from pyglet.graphics import *
from pyglet.window import Window

class MainWindow(Window):
    def __init__(self, simulation, width, height, config):
        super(MainWindow, self).__init__(width=width, height=height,
                                         caption='Cayley', config=config)
        self.simulation = simulation

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for body in self.simulation.bodies:
            position = body.position()
            x, y = position.x, position.y
            c = body.colour
            hw, hh = body.dimensions[0] / 2.0, body.dimensions[1] / 2.0
            draw(4, GL_QUADS,
                 ('v2f', (
                 x - hw, y + hh,
                 x + hw, y + hh,
                 x + hw, y - hh,
                 x - hw, y - hh)),
                 ('c3f', c * 4)
                 )

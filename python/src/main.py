from pyglet import *
from pyglet.gl import *
from pyglet.graphics import *
from cayley import *

WIDTH, HEIGHT = 640, 480
TIMESTEP = 1 / 60.0

class MainWindow(window.Window):
    def __init__(self, simulation, config=None):
        super(MainWindow, self).__init__(width=WIDTH, height=HEIGHT,
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


simulation = Simulation(WIDTH, HEIGHT)

simulation.add_body(position=(WIDTH / 2, 20), dimensions=(200, 20),
                    colour=(0.5, 1, 0.5))

simulation.add_body(position=(WIDTH / 2, 100), dimensions=(10, 10),
                    colour=(1, 1, 1), density=1, friction=0.3, restitution=0.5)

try:
    config = Config(sample_buffers=1, samples=4, depth_size=16,
                    double_buffer=True)
    MainWindow(simulation, config)
except window.NoSuchConfigException:
    MainWindow(simulation)

clock.schedule_interval(simulation.update, TIMESTEP)

app.run()

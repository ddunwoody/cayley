from simulation import Simulation
from pyglet import app
from pyglet import clock
from pyglet.gl import *
from pyglet.graphics import *
from pyglet.window import Window

WIDTH, HEIGHT = 640, 480
TIMESTEP = 1 / 60.0

simulation = Simulation(WIDTH, HEIGHT)

simulation.add_body(position=(WIDTH / 2, 20), dimensions=(200, 20),
                    colour=(0.5, 1, 0.5))

simulation.add_body(position=(WIDTH / 2, 100), dimensions=(10, 10),
                    colour=(1, 1, 1), density=1, friction=0.3, restitution=0.5)

config = Config(sample_buffers=1, samples=4, depth_size=16,
                double_buffer=True)
window = Window(width=WIDTH, height=HEIGHT, caption='Cayley', config=config)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    for body in simulation.bodies:
        body.draw()

clock.schedule_interval(simulation.update, TIMESTEP)
app.run()

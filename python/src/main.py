from pyglet import *
from pyglet.gl import *
from pyglet.window import *
from simulation import Simulation

TIMESTEP = 1 / 60.0
MARGIN = 0.1

display = get_platform().get_default_display()
screen = Display.get_default_screen(display)
window_scale = 1 - MARGIN * 2
width = int(screen.width * window_scale)
height = int(screen.height * window_scale)

simulation = Simulation(width, height)

simulation.add_body(position=(width / 2, 20), dimensions=(200, 20),
                    colour=(0.5, 1, 0.5))

simulation.add_body(position=(width / 2, 100), dimensions=(10, 10),
                    colour=(1, 1, 1), density=1, friction=0.3, restitution=0.5)


config = Config(sample_buffers=1, samples=4, depth_size=16,
                double_buffer=True)

window = Window(width=width, height=height, caption='Cayley', resizable=True,
                config=config, visible=False)
window.set_exclusive_mouse()

class Camera:
    init = False
    x = y = 0

camera = Camera()

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(camera.x, camera.y, 0)
    for body in simulation.bodies:
        body.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    if camera.init:
        camera.x += dx
        camera.y += dy
    else:
        camera.init = True

clock.schedule_interval(simulation.update, TIMESTEP)

window.set_visible()
window.set_location(int(screen.width * MARGIN), int(screen.height * MARGIN))
app.run()

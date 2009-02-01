from body import Polygon
from display import Window
from pyglet import app, clock
from world import World

world = World(10000, 10000)

ground = Polygon(colour=(0.5, 1, 0.5))
ground.setAsBox(200, 10)
world.add_body((1000, -10), ground)

box = Polygon(density=1, friction=0.3, restitution=0.5)
box.setAsBox(10, 10)
world.add_body((1000, 100), box)

window = Window(world, caption='Cayley', resizable=True, visible=False)
window.set_screen_margin(0.1)
window.focus_camera(1000, 0)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(world.update, 1 / 60.0)
app.run()

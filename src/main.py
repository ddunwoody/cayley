from polygon import Polygon
from display import Window
from pyglet import app, clock
from world import World

world = World(10000, 10000)

ground = Polygon(colour=(0.5, 1, 0.5))
ground.setAsBox(5000, 50)
world.add_body((0, -25), ground)

ship_vert_l = ((-10, -10),
               (0, -5),
               (0, 10),
               (-10, 0))
ship_vert_r = ((10, -10),
               (10, 0),
               (0, 10),
               (0, -5))

d, f, r = 1, 0.3, 0.2
ship_l = Polygon(vertices=ship_vert_l, density=d, friction=f, restitution=r)
ship_r = Polygon(vertices=ship_vert_r, density=d, friction=f, restitution=r)
world.add_body((0, 10), ship_l, ship_r)

window = Window(world, caption='Cayley', resizable=True, visible=False)
window.set_screen_margin(0.1)
window.focus_camera(0, 200)
window.set_zoom(2)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(world.update, 1 / 60.0)
app.run()

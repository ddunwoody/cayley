from display import Window
from shape import Circle, Polygon
from pyglet import app, clock
from world import World

world = World(10000, 10000)

ground = Polygon(colour=(0.5, 0.5, 0.5))
ground.setAsBox(5000, 1000)
world.add_body((0, -500), ground)

vert_b = ((-70, -10),
          (  0, -10),
          (  0,  -4),
          (-10,   0),
          (-68,   0))
vert_t = ((-60,   0),
          (-15,   0),
          (-30,  10),
          (-50,  10))

dens, fr, rest = 1, 0.3, 0.2
car_b = Polygon(vertices=vert_b, colour=(1.00, 0.25, 0.25),
                 density=dens, friction=fr, restitution=rest)
car_t = Polygon(vertices=vert_t, colour=(0.25, 0.25, 1.00),
                 density=dens, friction=fr, restitution=rest)
wheel_r = Circle((-55, -10), 5, colour=(0.50, 0.50, 0.75),
                 density=dens, friction=fr, restitution=rest)
wheel_f = Circle((-15, -10), 5, colour=(0.75, 0.50, 0.50),
                 density=dens, friction=fr, restitution=rest)
world.add_body((0, 17), car_b, car_t, wheel_r, wheel_f)

window = Window(world, caption='Cayley', resizable=True, visible=False)
window.set_screen_margin(0.1)
window.focus_camera(0, 200)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(world.update, 1/60.)
app.run()

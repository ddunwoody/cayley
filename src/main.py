from display import Window
from shape import Circle, Polygon
from pyglet import app, clock
from world import World
from Box2D import b2RevoluteJointDef

world = World(10000, 10000)

ground = Polygon(colour=(0.5, 0.5, 0.5))
ground.setAsBox(5000, 1000)
world.create_body((0, -500), ground)

vert_b = ((-70, -10),
          (  0, -10),
          (  0,  -4),
          (-10,   0),
          (-68,   0))
vert_t = ((-60,   0),
          (-15,   0),
          (-30,  10),
          (-50,  10))

chass_b = Polygon(vertices=vert_b, colour=(1.00, 0.25, 0.25),
                 density=20, friction=0.6)
chass_t = Polygon(vertices=vert_t, colour=(0.25, 0.25, 1.00),
                 density=5, friction=0.6)

chassis = world.create_body((0, 15), chass_b, chass_t)

circ_r = Circle(5, colour=(0.50, 0.50, 0.75), density=40, friction=0.8)
circ_f = Circle(5, colour=(0.75, 0.50, 0.50), density=40, friction=0.8)

wheel_r = world.create_body((-55, 5), circ_r)
wheel_f = world.create_body((-15, 5), circ_f)

jd = b2RevoluteJointDef()
jd.Initialize(chassis, wheel_r, wheel_r.GetWorldCenter())
jd.enableMotor = True
jd.maxMotorTorque = 50000
drive = world.create_joint(jd)

jd.Initialize(chassis, wheel_f, wheel_f.GetWorldCenter())
world.create_joint(jd)

window = Window(world, caption='Cayley', resizable=True, visible=False)
window.set_screen_margin(0.1)
window.focus_camera(0, 200)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(world.update, 1/60.)
app.run()

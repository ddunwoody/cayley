from display import Window
from pyglet import app, clock
from world import World

world = World(10000, 10000)

world.add_body(position=(500, 20), dimensions=(200, 20),
                    colour=(0.5, 1, 0.5))

world.add_body(position=(500, 100), dimensions=(10, 10),
                    colour=(1, 1, 1), density=1, friction=0.3, restitution=0.5)


window = Window(world, caption='Cayley', resizable=True, visible=False)
window.size_to_margin(0.1)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(world.update, 1 / 60.0)

app.run()

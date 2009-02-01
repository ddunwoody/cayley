from display import Window
from pyglet import app, clock
from simulation import Simulation

simulation = Simulation(10000, 10000)

simulation.add_body(position=(500, 20), dimensions=(200, 20),
                    colour=(0.5, 1, 0.5))

simulation.add_body(position=(500, 100), dimensions=(10, 10),
                    colour=(1, 1, 1), density=1, friction=0.3, restitution=0.5)


window = Window(simulation, caption='Cayley', resizable=True, visible=False)
window.size_to_margin(0.1)
window.set_visible()
window.center_on_screen()

clock.schedule_interval(simulation.update, 1 / 60.0)

app.run()

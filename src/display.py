from pyglet.gl import *
import pyglet

class Camera:
    has_moved = False
    x = y = 0
    
    def move_by(self, dx, dy):
        # don't move for the first event
        if self.has_moved:
            self.x += dx
            self.y += dy
        else:
            self.has_moved = True
        
class Window(pyglet.window.Window):
    def __init__(self, world, *args, **kwargs):
        config = Config(sample_buffers=1, samples=4, depth_size=16,
                        double_buffer=True)
        super(Window, self).__init__(config=config, *args, **kwargs)
        self.world = world
        self.camera = Camera()
        self.set_exclusive_mouse()

    def size_to_margin(self, margin):
        screen = self.screen
        border_width = int(self.screen.width * margin)
        border_height = int(self.screen.height * margin)
        self.width = screen.width - border_width * 2
        self.height = screen.height - border_height * 2

    def center_on_screen(self):
        x = (self.screen.width - self.width) / 2
        y = (self.screen.height - self.height) / 2
        self.set_location(x, y)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.camera.x, self.camera.y, 0)
        for body in self.world.bodies:
            body.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.camera.move_by(dx, dy)
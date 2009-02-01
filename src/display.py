from pyglet.gl import *
import pyglet

class Camera:
    x = y = 0
    _zoom = 1
    zoom_inc = 0.1

    def move(self, dx, dy):
        self.x += dx * 1 / self._zoom
        self.y += dy * 1 / self._zoom
    
    def zoom(self, factor):
        self._zoom += factor * self.zoom_inc
        if self._zoom < self.zoom_inc:
            self._zoom = self.zoom_inc

    def configure_gl_matrix(self, width, height):
        glLoadIdentity()
        hw, hh = width / 2, height / 2
        glTranslatef(hw, hh, 0)
        glScalef(self._zoom, self._zoom, 1)
        glTranslatef(-hw, -hh, 0)
        glTranslatef(self.x, self.y, 0)
        
class Window(pyglet.window.Window):
    def __init__(self, world, *args, **kwargs):
        config = Config(sample_buffers=1, samples=4, depth_size=16,
                        double_buffer=True)
        super(Window, self).__init__(config=config, *args, **kwargs)
        self.world = world
        self.camera = Camera()
        self.set_exclusive_mouse()

    def set_screen_margin(self, margin):
        screen = self.screen
        border_width = int(self.screen.width * margin)
        border_height = int(self.screen.height * margin)
        self.width = screen.width - border_width * 2
        self.height = screen.height - border_height * 2

    def center_on_screen(self):
        x = (self.screen.width - self.width) / 2
        y = (self.screen.height - self.height) / 2
        self.set_location(x, y)

    # move the camera such that the centre of the window looks at this point
    def focus_camera(self, x, y):
        self.camera.x = self.width / 2 - x
        self.camera.y = self.height / 2 - y

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.camera.configure_gl_matrix(self.width, self.height)
        for body in self.world.bodies:
            body.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        # ignore first motion
        if x != dx or y != dy:
            self.camera.move(dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.zoom(scroll_y)

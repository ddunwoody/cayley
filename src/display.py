from pyglet.gl import *
from pyglet.graphics import draw
import pyglet

class Camera:
    x = y = 0
    zoom = 1
    zoom_inc = 0.1

    def move(self, dx, dy):
        self.x += dx * 1 / self.zoom
        self.y += dy * 1 / self.zoom
    
    def adjust_zoom(self, factor):
        self.zoom += factor * self.zoom_inc
        if self.zoom < self.zoom_inc:
            self.zoom = self.zoom_inc

    def configure_gl_matrix(self, width, height):
        glLoadIdentity()
        hw, hh = width / 2, height / 2
        glTranslatef(hw, hh, 0)
        glScalef(self.zoom, self.zoom, 1)
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
        
    def set_zoom(self, zoom):
        self.camera.zoom = zoom

    def on_mouse_motion(self, x, y, dx, dy):
        # ignore first motion
        if x != dx or y != dy:
            self.camera.move(dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.adjust_zoom(scroll_y)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.camera.configure_gl_matrix(self.width, self.height)
        for item in self.world.render_list:
            body = item[0]
            polygons = item[1]
            for polygon in polygons:
                vertices = ()
                for vertex in polygon.shape.getVertices_b2Vec2():
                    vertices += body.GetWorldPoint(vertex).tuple()
                    glColor3f(polygon.colour[0], 
                              polygon.colour[1], 
                              polygon.colour[2])
                    draw(len(vertices) / 2, 
                         GL_POLYGON, 
                         ('v2f', vertices))


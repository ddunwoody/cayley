from Box2D import b2CircleDef, b2PolygonDef
from math import cos, pi, sin
from pyglet.gl import *
from pyglet.graphics import draw

class Shape(object):
    def __init__(self, shape=None, colour=(1,1,1), density=None,
                 friction=None, restitution=None):
        self.colour = colour
        self.shape = shape
        if density is not None:
            self.shape.density = density
        if friction is not None:
            self.shape.friction = friction
        if restitution is not None:
            self.shape.restitution = restitution

    def __str__(self):
        return "Shape(%s, colour: %s)" % (self.shape.__str__(), self.colour)

    def set_gl_color(self):
        glColor4f(self.colour[0], self.colour[1], self.colour[2], 0.5)

class Circle(Shape):
    def __init__(self, local_position, radius, colour=(1,1,1),
               density=None, friction=None, restitution=None):
        self.shape = b2CircleDef()
        super(Circle, self).__init__(shape=b2CircleDef(), colour=colour,
                                     density=density, friction=friction,
                                     restitution=restitution)
        self.shape.localPosition = local_position
        self.shape.radius = radius
        
    def draw(self, body):
        self.set_gl_color()
        points = 24
        step = 2 * pi / points
        radius = self.shape.radius
        centre = body.GetWorldPoint(self.shape.localPosition).tuple()
        vertices = ()
        n = 0
        for i in range(0, points):
            vertices += centre
            vertices += (cos(n) * radius + centre[0],
                         sin(n) * radius + centre[1])
            n += step 
            vertices += (cos(n) * radius + centre[0],
                         sin(n) * radius + centre[1])
            draw(len(vertices) / 2,
                 GL_POLYGON,
                 ('v2f', vertices))


class Polygon(Shape):
    def __init__(self, colour=(1,1,1), vertices=None,
                 density=None, friction=None, restitution=None):
        super(Polygon, self).__init__(shape=b2PolygonDef(), colour=colour,
                                      density=density, friction=friction,
                                      restitution=restitution)
        if vertices is not None:
            self.shape.setVertices(vertices)

    def setAsBox(self, x, y):
        hx, hy = x / 2, y / 2
        self.shape.setVertices(((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)))

    def draw(self, body):
        self.set_gl_color()
        vertices = ()
        for vertex in self.shape.getVertices_b2Vec2():
            vertices += body.GetWorldPoint(vertex).tuple()
            draw(len(vertices) / 2,
                 GL_POLYGON,
                 ('v2f', vertices))

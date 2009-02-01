from Box2D import *
from pyglet.gl import *
from pyglet.graphics import *

# Defines a coloured polygon with physical properties
class Polygon:
    def __init__(self, colour=(1, 1, 1),
                 density=None, friction=None, restitution=None):
        self.shape = b2PolygonDef()
        self.colour = colour
        if density is not None:
            self.shape.density = density
        if friction is not None:
            self.shape.friction = friction
        if restitution is not None:
            self.shape.restitution = restitution

    def setAsBox(self, x, y):
        hx, hy = x / 2, y / 2
        self.shape.setVertices(((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)))

# binds a polygon to its physics representation so it can be drawn
class Body:
    def __init__(self, body, polygon):
        self.body = body
        self.polygon = polygon

    def draw(self):
        vertices = ()
        for vertex in self.polygon.shape.getVertices_b2Vec2():
            vertices += self.body.GetWorldPoint(vertex).tuple()
        glColor3f(self.polygon.colour[0], 
                  self.polygon.colour[1], 
                  self.polygon.colour[2])
        draw(len(vertices) / 2, 
             GL_POLYGON, 
             ('v2f', vertices))


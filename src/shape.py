from Box2D import b2CircleDef, b2PolygonDef
from render import draw_circle, draw_polygon, set_color

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


class Circle(Shape):
    def __init__(self, radius, local_position=(0,0), colour=(1,1,1),
               density=None, friction=None, restitution=None):
        self.shape = b2CircleDef()
        super(Circle, self).__init__(shape=b2CircleDef(), colour=colour,
                                     density=density, friction=friction,
                                     restitution=restitution)
        self.shape.localPosition = local_position
        self.shape.radius = radius
        
    def draw(self, body):
        center = body.GetWorldPoint(self.shape.localPosition).tuple()
        axis = body.angle
        radius = self.shape.radius
        set_color(self.colour)
        draw_circle(center, axis, radius)


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
        vertices = ()
        for vertex in self.shape.getVertices_b2Vec2():
            vertices += body.GetWorldPoint(vertex).tuple()
        set_color(self.colour)
        draw_polygon(vertices)

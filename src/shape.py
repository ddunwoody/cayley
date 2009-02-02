from Box2D import b2CircleDef, b2PolygonDef

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
    def __init__(self, local_position, radius, colour=(1,1,1),
               density=None, friction=None, restitution=None):
        self.shape = b2CircleDef()
        super(Circle, self).__init__(shape=b2CircleDef(), colour=colour,
                                     density=density, friction=friction,
                                     restitution=restitution)
        self.shape.localPosition = local_position
        self.shape.radius = radius


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

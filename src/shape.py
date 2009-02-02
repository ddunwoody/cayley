from Box2D import b2CircleDef, b2PolygonDef

class Circle:
    def __init__(self, local_position, radius, colour=(1,1,1),
               density=None, friction=None, restitution=None):
        self.shape = b2CircleDef()
        self.shape.localPosition = local_position
        self.shape.radius = radius
        self.colour = colour
        if density is not None:
            self.shape.density = density
        if friction is not None:
            self.shape.friction = friction
        if restitution is not None:
            self.shape.restitution = restitution
    def __str__(self):
        return "Circle(%s, colour: %s)" % (self.shape.__str__(), self.colour)

class Polygon:
    def __init__(self, colour=(1,1,1), vertices=None,
                 density=None, friction=None, restitution=None):
        self.shape = b2PolygonDef()
        self.colour = colour
        if vertices is not None:
            self.shape.setVertices(vertices)
        if density is not None:
            self.shape.density = density
        if friction is not None:
            self.shape.friction = friction
        if restitution is not None:
            self.shape.restitution = restitution

    def setAsBox(self, x, y):
        hx, hy = x / 2, y / 2
        self.shape.setVertices(((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)))
        
    def __str__(self):
        return "Polygon(%s, colour: %s)" % (self.shape.__str__(), self.colour)


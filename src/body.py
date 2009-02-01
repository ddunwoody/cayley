from Box2D import *
from pyglet.gl import *
from pyglet.graphics import *

class Body:
    def __init__(self, simulation, position, dimensions, colour, density=None,
                 friction=None, restitution=None):
        self.colour = colour
        self.dimensions = dimensions
        body_def = b2BodyDef()
        body_def.position = position
        self.body = simulation.world.CreateBody(body_def)
        shape_def = b2PolygonDef()
        shape_def.SetAsBox(dimensions[0] / 2.0, dimensions[1] / 2.0)
        if density is not None:
            shape_def.density = density
        if friction is not None:
            shape_def.friction = friction
        if restitution is not None:
            shape_def.restitution = restitution
        self.body.CreateShape(shape_def)
        if density is not None:
            self.body.SetMassFromShapes()

    def draw(self):
        vertices = ()
        for shape in self.body.GetShapeList():
            for vertex in shape.getVertices_b2Vec2():
                vertices += self.body.GetWorldPoint(vertex).tuple()
        glColor3f(self.colour[0], self.colour[1], self.colour[2])
        draw(len(vertices) / 2, GL_POLYGON, ('v2f', vertices))


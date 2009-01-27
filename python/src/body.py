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
        b = self.body
        x, y = b.position.x, b.position.y
        c = self.colour
        hw, hh = self.dimensions[0] / 2.0, self.dimensions[1] / 2.0
        draw(4, GL_QUADS,
             ('v2f', (
             x - hw, y + hh,
             x + hw, y + hh,
             x + hw, y - hh,
             x - hw, y - hh)),
             ('c3f', c * 4)
             )


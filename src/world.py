from Box2D import b2AABB, b2BodyDef, b2World
from body import Body

class World:
    VELOCITY_ITERATIONS = 8
    POSITION_ITERATIONS = 1

    def __init__(self, width, height):
        self.bodies = []
        aabb = b2AABB()
        aabb.lowerBound = (0, 0)
        aabb.upperBound = (width, height)
        gravity = (0, -10)
        do_sleep = True
        self.world = b2World(aabb, gravity, do_sleep)

    def update(self, dt):
        self.world.Step(dt, self.VELOCITY_ITERATIONS,
                        self.POSITION_ITERATIONS)

    def add_body(self, position, polygon):
        body_def = b2BodyDef()
        body_def.position = position
        body = self.world.CreateBody(body_def)
        body.CreateShape(polygon.shape)
        if polygon.shape.density is not None:
            body.SetMassFromShapes()
        self.bodies.append(Body(body, polygon))

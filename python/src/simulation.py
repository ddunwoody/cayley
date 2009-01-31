from Box2D import *
from body import Body

class Simulation:
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

    def add_body(self, *args, **kw):
        self.bodies.append(Body(self, *args, **kw))

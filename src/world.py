from Box2D import b2AABB, b2BodyDef, b2World

class World:
    VELOCITY_ITERATIONS = 8
    POSITION_ITERATIONS = 1

    def __init__(self, width, height):
        self.render_list = []
        aabb = b2AABB()
        aabb.lowerBound = (-width, -height)
        aabb.upperBound = (width, height)
        gravity = (0, -10)
        do_sleep = True
        self.world = b2World(aabb, gravity, do_sleep)

    def update(self, dt):
        self.world.Step(dt, self.VELOCITY_ITERATIONS,
                        self.POSITION_ITERATIONS)

    def add_body(self, position, *polygons):
        body_def = b2BodyDef()
        body_def.position = position
        body = self.world.CreateBody(body_def)
        for polygon in polygons:
            body.CreateShape(polygon.shape)
            if polygon.shape.density is not None:
                body.SetMassFromShapes()
        self.render_list.append((body, polygons))



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

    def create_body(self, position, *shapes):
        body_def = b2BodyDef()
        body_def.position = position
        body = self.world.CreateBody(body_def)
        for shape in shapes:
            body.CreateShape(shape.shape)
            if shape.shape.density is not None:
                body.SetMassFromShapes()
        self.render_list.append((body, shapes))
        return body

    def create_joint(self, joint_def):
        return self.world.CreateJoint(joint_def).getAsType()

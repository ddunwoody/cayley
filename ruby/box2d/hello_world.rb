#!/usr/bin/env ruby

require 'box2d'
include Box2d

# This is a simple example of building and running a simulation
# using Box2D. Here we create a large ground box and a small dynamic
# box.

# Define the size of the world. Simulation will still work
# if bodies reach the end of the world, but it will be slower.

worldAABB = B2AABB.new
worldAABB.lowerBound.Set -100, -100
worldAABB.upperBound.Set 100, 100

# Define the gravity vector.
gravity = B2Vec2.new 0, -10

# Do we want to let bodies sleep?
doSleep = true

# Construct a world object, which will hold and simulate the rigid bodies.
world = B2World.new worldAABB, gravity, doSleep

# Define the ground body.
groundBodyDef = B2BodyDef.new
groundBodyDef.position.Set 0, -10

# Call the body factory which allocates memory for the ground body
# from a pool and creates the ground box shape (also from a pool).
# The body is also added to the world.
groundBody = world.CreateBody groundBodyDef

# Define the ground box shape.
groundShapeDef = B2PolygonDef.new

# The extents are the half-widths of the box.
groundShapeDef.SetAsBox 50, 10

# Add the ground shape to the ground body.
groundBody.CreateShape groundShapeDef

# Define the dynamic body. We set its position and call the body factory.
bodyDef = B2BodyDef.new
bodyDef.position.Set 0, 4
body = world.CreateBody bodyDef

# Define another box shape for our dynamic body.
shapeDef = B2PolygonDef.new
shapeDef.SetAsBox 1, 1

# Set the box density to be non-zero, so it will be dynamic.
shapeDef.density = 1

# Override the default friction.
shapeDef.friction = 0.3

# Add the shape to the body.
body.CreateShape shapeDef

# Now tell the dynamic body to compute it's mass properties base
# on its shape.
body.SetMassFromShapes

# Prepare for simulation. Typically we use a time step of 1/60 of a
# second (60Hz) and 10 iterations. This provides a high quality simulation
# in most game scenarios.
timeStep = 1 / 60.0
velocityIterations = 8
positionIterations = 1

# This is our little game loop.
60.times do
  # Instruct the world to perform a single step of simulation. It is
  # generally best to keep the time step and iterations fixed.
  world.Step timeStep, velocityIterations, positionIterations

  # Now print the position and angle of the body.
  position = body.GetPosition
  angle = body.GetAngle
  printf "%4.2f %4.2f %4.2f\n", position.x, position.y, angle
end


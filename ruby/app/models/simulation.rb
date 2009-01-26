module Simulation
  VELOCITY_ITERATIONS = 8
  POSITION_ITERATIONS = 1

  @@bodies = []

  aabb = B2AABB.new
  aabb.lowerBound.Set 0, 0
  aabb.upperBound.Set WIDTH, HEIGHT

  gravity = B2Vec2.new 0, -10
  do_sleep = true
  @@world = B2World.new aabb, gravity, do_sleep

  def self.add_body(&block)
    @@bodies << Body.new(Body::Configuration.new(&block))
  end

  def self.update
    @@world.Step TIMESTEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS
  end

  def self.bodies
    @@bodies
  end

  def self.world
    @@world
  end

  def self.draw window
    @@bodies.each do |body|
      position = body.position
      x, y = position.x, HEIGHT-position.y
      hw, hh = body.dimensions.x / 2.0, body.dimensions.y / 2.0
      c = body.colour
      window.draw_quad x-hw, y-hh, c, x+hw, y-hh, c, x-hw, y+hh, c, x+hw, y+hh, c
    end
  end
end

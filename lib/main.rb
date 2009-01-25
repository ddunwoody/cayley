#!/usr/bin/env ruby

require 'rubygems'

require 'gosu'
require 'box2d'

include Gosu
include Box2d

WIDTH = 640
HEIGHT = 480
TIMESTEP = 1/60.0
VELOCITY_ITERATIONS = 8
POSITION_ITERATIONS = 1

class World
  attr_reader :body, :ground

  def initialize
    aabb = B2AABB.new
    aabb.lowerBound.Set 0, 0
    aabb.upperBound.Set WIDTH, HEIGHT

    gravity = B2Vec2.new 0, -10
    do_sleep = true
    @world = B2World.new aabb, gravity, do_sleep

    # Define the ground body.
    ground_body_def = B2BodyDef.new
    ground_body_def.position.Set WIDTH/2, 20

    # Call the body factory which allocates memory for the ground body
    # from a pool and creates the ground box shape (also from a pool).
    # The body is also added to the world.
    @ground = @world.CreateBody ground_body_def

    # Define the ground box shape.
    ground_shape_def = B2PolygonDef.new

    # The extents are the half-widths of the box.
    ground_shape_def.SetAsBox 100, 10

    # Add the ground shape to the ground body.
    @ground.CreateShape ground_shape_def

    # Define the dynamic body. We set its position and call the body factory.
    body_def = B2BodyDef.new
    body_def.position.Set WIDTH/2, 100
    @body = @world.CreateBody body_def

    # Define another box shape for our dynamic body.
    shape_def = B2PolygonDef.new
    shape_def.SetAsBox 5, 5

    shape_def.density = 1
    shape_def.friction = 0.3
    shape_def.restitution = 0.5

    # Add the shape to the body.
    @body.CreateShape shape_def

    # Now tell the dynamic body to compute it's mass properties base
    # on its shape.
    @body.SetMassFromShapes
  end

  def update
    @world.Step TIMESTEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS

    # Now print the position and angle of the body.
    position = @body.GetPosition
    angle = @body.GetAngle
    printf "%4.2f %4.2f %4.2f\n", position.x, position.y, angle
  end
end

class MainWindow < Window
  def initialize
    super WIDTH, HEIGHT, false, TIMESTEP
    self.caption = 'Cayley'
    @world = World.new
  end

  def update
    @world.update
  end

  def draw
    position = @world.body.GetPosition
    x, y = position.x, HEIGHT-position.y
    c = 0xFFFFFFFF
    draw_quad x-5, y-5, c, x+5, y-5, c, x-5, y+5, c, x+5, y+5, c

    position = @world.ground.GetPosition
    x, y = position.x, HEIGHT-position.y
    c = 0xFF80FF80
    draw_quad x-100, y-10, c, x+100, y-10, c, x-100, y+10, c, x+100, y+10, c
  end

  def button_down id
    if id == Button::KbEscape then
      close
    end
  end
end

MainWindow.new.show

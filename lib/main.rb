#!/usr/bin/env ruby

require 'rubygems'

require 'gosu'
require 'box2d'
require 'singleton'

include Gosu
include Box2d

WIDTH = 640
HEIGHT = 480
TIMESTEP = 1/60.0
VELOCITY_ITERATIONS = 8
POSITION_ITERATIONS = 1

class Simulation
  include Singleton
  attr_reader :body, :ground, :world, :bodies

  def initialize
    @bodies = []
    aabb = B2AABB.new
    aabb.lowerBound.Set 0, 0
    aabb.upperBound.Set WIDTH, HEIGHT

    gravity = B2Vec2.new 0, -10
    do_sleep = true
    @world = B2World.new aabb, gravity, do_sleep

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

  def add_body(&block)
    @bodies << Body.new(&block)
  end

  def update
    @world.Step TIMESTEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS
    # Now print the position and angle of the body.
    position = @body.GetPosition
    angle = @body.GetAngle
    printf "%4.2f %4.2f %4.2f\n", position.x, position.y, angle
  end

end

class Body
  attr_accessor :position, :colour

  def initialize
    body_def = B2BodyDef.new
    raise 'A block must be given' unless block_given?
    yield self
    raise 'Position must be set' if position.nil?
    body_def.position.Set @position[0], @position[1]
    body = Simulation.instance.world.CreateBody body_def
    body.CreateShape @shape_def
  end

  def set_as_box half_width, half_height
    @shape_def = B2PolygonDef.new
    @shape_def.SetAsBox half_width, half_height
  end
end

class MainWindow < Window
  def initialize
    super WIDTH, HEIGHT, false, TIMESTEP
    self.caption = 'Cayley'
    Simulation.instance.add_body do |body|
      body.position = WIDTH/2, 20
      body.set_as_box 100, 10
      body.colour = 0xFF7FFF7F
    end
  end

  def update
    Simulation.instance.update
  end

  def draw
    position = Simulation.instance.body.GetPosition
    x, y = position.x, HEIGHT-position.y
    c = 0xFFFFFFFF
    draw_quad x-5, y-5, c, x+5, y-5, c, x-5, y+5, c, x+5, y+5, c

    Simulation.instance.bodies.each do |body|
      position = body.position
      x, y = position[0], HEIGHT-position[1]
      c = body.colour
      draw_quad x-100, y-10, c, x+100, y-10, c, x-100, y+10, c, x+100, y+10, c
    end
  end

  def button_down id
    if id == Button::KbEscape then
      close
    end
  end
end

MainWindow.new.show

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

  def self.add_body(*args, &block)
    @@bodies << Body.new(*args, &block)
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
end

class Body
  attr_accessor :colour, :density, :friction, :half_height, :half_width,
    :restitution

  def initialize x, y
    raise 'A block must be given' unless block_given?
    yield self
    body_def = B2BodyDef.new
    body_def.position.Set x, y

    @body = Simulation.world.CreateBody body_def

    shape_def = B2PolygonDef.new
    shape_def.SetAsBox @half_width, @half_height
    shape_def.density = @density if @density
    shape_def.friction = @friction if @friction
    shape_def.restitution = @restitution if @restitution

    @body.CreateShape shape_def
    @body.SetMassFromShapes if @density
  end

  def set_as_box half_width, half_height
    @half_width, @half_height = half_width, half_height
  end

  def position
    @body.GetPosition
  end

  def angle
    @body.GetAngle
  end
end

class MainWindow < Window
  def initialize
    super WIDTH, HEIGHT, false, TIMESTEP
    self.caption = 'Cayley'
    Simulation.add_body(WIDTH/2, 20) do |body|
      body.set_as_box 100, 10
      body.colour = 0xFF7FFF7F
    end

    Simulation.add_body(WIDTH/2, 100) do |body|
      body.set_as_box 5, 5
      body.colour = 0xFFFFFFFF
      body.density = 1
      body.friction = 0.3
      body.restitution = 0.5
    end
  end

  def update
    Simulation.update
  end

  def draw
    Simulation.bodies.each do |body|
      position = body.position
      x, y = position.x, HEIGHT-position.y
      hw, hh = body.half_width, body.half_height
      c = body.colour
      draw_quad x-hw, y-hh, c, x+hw, y-hh, c, x-hw, y+hh, c, x+hw, y+hh, c
    end
  end

  def button_down id
    if id == Button::KbEscape then
      close
    end
  end
end

MainWindow.new.show

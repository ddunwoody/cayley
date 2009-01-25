#!/usr/bin/env ruby

require 'rubygems'

require 'gosu'
require 'box2d'

include Gosu
include Box2d

WIDTH = 640
HEIGHT = 480
TIMESTEP = 1 / 60.0

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

class Vector
  attr_accessor :x, :y

  def initialize x, y
    @x, @y = x, y
  end
end

class Body
  attr_reader :colour, :dimensions

  def initialize config
    @colour, @dimensions = config.colour, config.dimensions
    body_def = B2BodyDef.new
    body_def.position.Set config.position[0], config.position[1]

    @body = Simulation.world.CreateBody body_def

    shape_def = B2PolygonDef.new
    shape_def.SetAsBox @dimensions.x / 2.0, @dimensions.y / 2.0
    shape_def.density = config.density if config.density
    shape_def.friction = config.friction if config.friction
    shape_def.restitution = config.restitution if config.restitution

    @body.CreateShape shape_def
    @body.SetMassFromShapes if config.density
  end

  def position
    @body.GetPosition
  end

  class Configuration
    attr_accessor :colour, :density, :friction, :position, :restitution
    attr_reader :dimensions

    def initialize
      raise 'A block must be given' unless block_given?
      yield self
      raise 'position must be set' unless @position
      raise 'dimensions must be set' unless @dimensions
      raise 'colour must be set' unless @colour
    end

    def dimensions= dimensions
      if dimensions.is_a? Vector
        @dimensions = dimensions
      elsif dimensions.respond_to? :length and dimensions.length == 2
        @dimensions = Vector.new dimensions[0], dimensions[1]
      end
    end
  end
end

class MainWindow < Window
  def initialize
    super WIDTH, HEIGHT, false, TIMESTEP
    self.caption = 'Cayley'

    Simulation.add_body do |body|
      body.position = WIDTH/2, 20
      body.dimensions = 200, 20
      body.colour = 0xFF7FFF7F
    end

    Simulation.add_body do |body|
      body.position = WIDTH/2, 100
      body.dimensions = 10, 10
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
    Simulation.draw self
  end

  def button_down id
    if id == Button::KbEscape then
      close
    end
  end
end

MainWindow.new.show

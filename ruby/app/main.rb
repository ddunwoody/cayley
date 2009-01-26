#!/usr/bin/env ruby

require 'rubygems'

require 'gosu'
require 'box2d'

include Gosu
include Box2d

WIDTH = 640
HEIGHT = 480
TIMESTEP = 1 / 60.0

Dir[File.join(File.dirname(__FILE__), 'models/*.rb')].each do |file|
  require file
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

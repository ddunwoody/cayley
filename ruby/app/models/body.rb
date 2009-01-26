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

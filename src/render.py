from math import cos, pi, sin
from pyglet.gl import *
from pyglet.graphics import draw

def draw_polygon(colour, vertices):
    glColor4f(colour[0], colour[1], colour[2], 0.5)
    draw(len(vertices) / 2, GL_POLYGON, ('v2f', vertices))

def draw_circle(colour, center, radius):
    NUM_POINTS = 24
    step = 2 * pi / NUM_POINTS
    vertices = ()
    n = 0
    for i in range(0, NUM_POINTS):
        vertices += center
        vertices += (cos(n) * radius + center[0],
                     sin(n) * radius + center[1])
        n += step 
        vertices += (cos(n) * radius + center[0],
                     sin(n) * radius + center[1])
    draw_polygon(colour, vertices)

from math import cos, pi, sin
from pyglet.gl import *
from pyglet.graphics import draw

def set_color(color):
    glColor4f(color[0], color[1], color[2], 0.5)

def draw_line_loop(vertices):
    draw(len(vertices) / 2, GL_LINE_LOOP, ('v2f', vertices))

def draw_polygon(vertices):
    draw(len(vertices) / 2, GL_POLYGON, ('v2f', vertices))
    draw_line_loop(vertices)

def draw_lines(vertices):
    draw(len(vertices) / 2, GL_LINES, ('v2f', vertices))

def draw_circle(center, axis, radius):
    NUM_POINTS = 24
    step = 2 * pi / NUM_POINTS
    vertices = ()
    n = 0
    for i in range(0, NUM_POINTS):
        vertices += (cos(n) * radius + center[0],
                     sin(n) * radius + center[1])
        n += step 
        vertices += (cos(n) * radius + center[0],
                     sin(n) * radius + center[1])
    draw_polygon(vertices)
    draw_lines((center[0], center[1],
                cos(axis) * radius + center[0], sin(axis) * radius + center[1]))

"""
alinen 2020
QWOP clone written with pyglet and pymunk
"""

import math
import pymunk, pymunk.pyglet_util
from pymunk.vec2d import Vec2d
import pyglet
from pyglet.window import key
from character import Character

window = pyglet.window.Window()
fps_display = pyglet.window.FPSDisplay(window=window)
label = pyglet.text.Label('0 meters',
                          font_name='Times New Roman',
                          font_size=24,
                          x=window.width//2, y=window.height*0.9,
                          anchor_x='center', anchor_y='center')
character = None
qDown = False
wDown = False
oDown = False
pDown = False
paused = False
debug_draw = False

@window.event
def on_key_release(symbol, modifiers):
    global qDown
    global wDown
    global oDown
    global pDown
    if symbol == key.Q:
        qDown = False
    elif symbol == key.W:
        wDown = False
    elif symbol == key.O:
        oDown = False
    elif symbol == key.P:
        pDown = False

@window.event
def on_key_press(symbol, modifiers):
    global qDown
    global wDown
    global oDown
    global pDown
    global paused
    global debug_draw
    qDown = wDown = oDown = pDown = False
    if symbol == key.ESCAPE:
        window.close()
    elif symbol == key.R:
        character.reset()
    elif symbol == key.Q:
        qDown = True
    elif symbol == key.W:
        wDown = True
    elif symbol == key.O:
        oDown = True
    elif symbol == key.P:
        pDown = True
    elif symbol == key.S:
        step()
    elif symbol == key.SPACE:
        paused = not paused
    elif symbol == key.D:
        debug_draw = not debug_draw

def print_commands():
    print("SPACE: Pause simulation")
    print("S: Step simulation")
    print("R: Reset character")
    print("D: Toggle debug draw of physics objects")
    print("Q: Apply force to left thigh")
    print("W: Apply force to right thigh")
    print("O: Apply force to left calf")
    print("P: Apply force to right calf")

def draw_rect(h1, h2, c1, c2):
    w = window.width
    h = window.height

    lc = character.get_position()[0] - w//2
    background = (lc, h*h1, w+lc, h*h1, w+lc, h*h2, lc, h*h2)
    colors = (c1[0],c1[1],c1[2],c1[3], 
              c1[0],c1[1],c1[2],c1[3], 
              c2[0],c2[1],c2[2],c2[3], 
              c2[0],c2[1],c2[2],c2[3])
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', background), ('c4B', colors))

def draw_white_line(h):
    draw_rect(h, h+0.01, (255,255,255,255), (255,255,255,100))
    draw_rect(h-0.01, h, (255,255,255,100), (255,255,255,255))

def draw_start():
    x = window.width/2
    h = window.height
    
    w1 = 25
    w2 = 10
    line1 = (x-w1, 10/h,  x, 10/h, x, h*0.28, x-w2, h*0.28)
    line2 = (x, 10/h,  x+w1, 10/h, x+w2, h*0.28, x, h*0.28)
    color1 = (255,255,255,50, 
              255,255,255,255, 
              255,255,255,255, 
              255,255,255,50)
    color2 = (255,255,255,255, 
              255,255,255,50, 
              255,255,255,50, 
              255,255,255,255)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', line1), ('c4B', color1))
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', line2), ('c4B', color2))

@window.event
def on_draw():
    window.clear()

    w = window.width
    h = window.height
    lc = character.get_position()[0] - w//2

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(lc, lc+w, 0, h, -1, 1)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    draw_rect(0.5, 1.0, (0,0,255,255), (0,0,50,255))
    draw_rect(0.45, 0.5, (0,200,0,255), (0,0,255,255))
    draw_rect(0.45, 0.35, (0,200,0,255), (0,200,0,255))
    draw_rect(0.35, 0.25, (0,200,0,255), (200,0,0,255))
    draw_rect(10/h, 0.25, (200,0,0,255), (200,0,0,255))
    draw_white_line(0.1)
    draw_white_line(0.2)
    draw_white_line(0.25)
    draw_white_line(0.28)
    draw_start()

    if debug_draw:
        fps_display.draw()
        options = pymunk.pyglet_util.DrawOptions()
        space.debug_draw(options)
    else:
        character.draw()

    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(0, w, 0, h, -1, 1)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    factor = 1.25/200
    label.text = "%.1f meters"%(lc * factor)
    label.draw()

def step():
    for x in range(10):
        space.step(1/50/10/2)

def update(dt):
    if qDown:
        character.move_thighL()
    elif wDown:
        character.move_thighR()
    elif oDown:
        character.move_calfL()
    elif pDown:
        character.move_calfR()

    if not paused:
       step()

def setup_world():
    space = pymunk.Space()
    space.gravity = 0,-9820
    space.damping = 0.99

    handler = space.add_collision_handler(100, 1)
    handler.begin = hit_ground

    floorHeight = 10
    floor = pymunk.Segment(space.static_body, Vec2d(-window.width*100,floorHeight), Vec2d(window.width*100,10), 1)
    floor.friction = 10.3
    floor.collision_type = 100
    space.add(floor)

    w = 100
    h = 200
    bodyx = window.width // 2
    bodyy = floorHeight + h + h/8 + 10 
    print("Body start", bodyx, bodyy)
    global character
    character = Character(space, bodyx, bodyy, 100, 200)

    return space

def hit_ground(arbiter, space, data):
    print("hit ground!")
    return True

print_commands()
space = setup_world()
pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
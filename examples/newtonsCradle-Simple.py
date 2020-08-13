# Pymunk example
# See http://www.pymunk.org/en/latest/examples.html
# See https://github.com/viblo/pymunk/blob/master/examples/newtons_cradle.ipynb 

import pymunk, pyglet, pymunk.pyglet_util
from pymunk.vec2d import Vec2d
from pyglet.window import key

window = pyglet.window.Window()
#pyglet.gl.glClearColor(240,240,240,255)
fps_display = pyglet.window.FPSDisplay(window=window)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()
    elif symbol == key.SPACE:
        space.shapes[1].body.apply_impulse_at_local_point((-12000,0))
        
@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    options = pymunk.pyglet_util.DrawOptions()
    space.debug_draw(options)

def update(dt):
    for x in range(10):
        space.step(1/50/10/2)

def setup_space():
    space = pymunk.Space()
    space.gravity = 0,-9820
    space.damping = 0.99
    return space

def setup_balls(space):
    width = 600
    height = 600
    for x in range(-100,150,50):
        x += width / 2
        offset_y = height/2
        mass = 10
        radius = 25
        moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, moment)
        body.position = x, -125+offset_y
        body.start_position = Vec2d(body.position)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = 0.9999999
        space.add(body, shape)
        pj = pymunk.PinJoint(space.static_body, body, (x, 125+offset_y), (0,0))
        space.add(pj)

space = setup_space()
setup_balls(space)

pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()

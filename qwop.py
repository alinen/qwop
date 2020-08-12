import math
import pymunk, pyglet, pymunk.pyglet_util
from pyglet.gl import *
from pymunk.vec2d import Vec2d
from pyglet.window import key

window = pyglet.window.Window()
fps_display = pyglet.window.FPSDisplay(window=window)
thighL = None
thighR = None
calfL = None
calfR = None
qDown = False
wDown = False
oDown = False
pDown = False
paused = True

def reset():
    for body in space.bodies:
        body.position = body.start_position
        body.angle = 0

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
    qDown = wDown = oDown = pDown = False
    if symbol == key.ESCAPE:
        window.close()
    elif symbol == key.R:
        reset()
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
        
@window.event
def on_draw():
    window.clear()
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(0, 680, 0, 480, -1, 1)
    glMatrixMode(pyglet.gl.GL_MODELVIEW)
    fps_display.draw()
    options = pymunk.pyglet_util.DrawOptions()
    space.debug_draw(options)

    pyglet.gl.glColor3f(.8,.8,.0)
    pyglet.gl.glPointSize(10)
    pyglet.graphics.draw(2, pyglet.gl.GL_POINTS, ('v2f',[0,0, 0, 100]))

def step():
    for x in range(10):
        space.step(1/50/10/2)

def update(dt):
    if qDown:
        thighL.apply_impulse_at_local_point((90, 0), (0, 0))
    elif wDown:
        thighR.apply_impulse_at_local_point((90, 0), (0, 0))
    elif oDown:
        calfL.apply_impulse_at_local_point((-90, 0), (0, 0))
    elif pDown:
        calfR.apply_impulse_at_local_point((-90, 0), (0, 0))

    if not paused:
       step()

def setup_space():
    space = pymunk.Space()
    space.gravity = 0,-9820
    space.damping = 0.99
    return space

def setup_body(space, centerx, centery, mass, width, height, collisionType, groupId = 1):
    moment = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, moment)
    body.position = centerx, centery
    body.start_position = Vec2d(body.position)
    body.width = width
    body.height = height
    
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.3
    shape.collision_type = collisionType
    shape.filter = pymunk.ShapeFilter(group=1)
    shape.group = groupId
    space.add(body, shape)
    return body

def hit_ground(arbiter, space, data):
    print("hit ground!")
    return True

def create_joint(space, b1, b2, px, py, lim1, lim2):
    """
    b1, b2: Body objects
    px, py: (float) Pivot point in world coordinates
    lim1, lim2: (float)  joint rotation limits (radians)
    """
    b1_b2 = pymunk.PivotJoint(b1, b2, (px, py))
    b1_b2.collide_bodies = False
    space.add(b1_b2)

    b1_b2_limit = pymunk.RotaryLimitJoint(b1, b2, -math.pi/10, math.pi/10)
    space.add(b1_b2_limit)

def setup_character(space):

    handler = space.add_collision_handler(100, 1)
    handler.begin = hit_ground

    floorHeight = 10
    floor = pymunk.Segment(space.static_body, Vec2d(-window.width,floorHeight), Vec2d(window.width*2,10), 1)
    floor.friction = 0.3
    floor.collision_type = 100
    space.add(floor)

    mass = 20
    h = 200
    w = 100
    bodyx = window.width // 2
    bodyy = floorHeight + h + h/8 + 10 # 10 = margin

    global thighL, thighR, calfL, calfR

    torso = setup_body(space, bodyx+0, bodyy+h*3/8, mass*2, w, h*3/4, 1, 2)
    head = setup_body(space, bodyx+0, bodyy+h*7/8, mass/2.0, w/2, w, 1, 2)

    thighL = setup_body(space, bodyx-w/4.0, bodyy-h/4.0, mass, w/2.0, h/2.0, 2)
    thighR = setup_body(space, bodyx+w/4.0, bodyy-h/4.0, mass, w/2.0, h/2.0, 2)

    calfL = setup_body(space, bodyx-w/4.0, bodyy-h*3/4.0, mass, w/2.0, h/2.0, 2)
    calfR = setup_body(space, bodyx+w/4.0, bodyy-h*3/4.0, mass, w/2.0, h/2.0, 2)

    footL = setup_body(space, bodyx-w/4+w/8, bodyy-h*17/16, mass/2.0, w*3/4, h/8, 2)
    footR = setup_body(space, bodyx+w/4+w/8, bodyy-h*17/16, mass/2.0, w*3/4, h/8, 2)

    create_joint(space, torso,  head,   bodyx,       bodyy+h*3/4, -math.pi/10,  math.pi/10)
    create_joint(space, torso,  thighL, bodyx-w/4,   bodyy      , -math.pi*3/4, math.pi/2)
    create_joint(space, torso,  thighR, bodyx+w/4,   bodyy      , -math.pi*3/4, math.pi/2)
    create_joint(space, thighL, calfL,  bodyx-w/4.0, bodyy-h/2.0, -math.pi/2,  -math.pi/10 )
    create_joint(space, thighR, calfR,  bodyx+w/4.0, bodyy-h/2.0, -math.pi/2,  -math.pi/10)
    create_joint(space, calfL,  footL,  bodyx-w/4.0, bodyy-h    , -math.pi/10,  math.pi/10)
    create_joint(space, calfR,  footR,  bodyx+w/4.0, bodyy-h    , -math.pi/10,  math.pi/10)

    ## For debugging
    ##torso_pin = pymunk.PinJoint(torso, space.static_body, (0,h*3/8), (bodyx, bodyy))
    ##space.add(torso_pin)

    #angle = -math.pi/6
    #rx = 0
    #ry = thighL.height / 2
    #off_x = math.cos(angle) * rx - math.sin(angle) * ry
    #off_y = math.sin(angle) * rx + math.cos(angle) * ry
    #thighL.position = (thighL.position[0] + rx - off_x, thighL.position[1] + ry - off_y)
    #print(rx, ry, off_x, off_y, thighL.position)
    #thighL.angle = angle

    #calfL.angle = -math.pi/4

space = setup_space()
setup_character(space)

pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
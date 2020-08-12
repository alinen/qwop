import math
import pyglet
import pymunk, pymunk.pyglet_util
from pymunk.vec2d import Vec2d

class Character:

    def __init__(self, space, bodyx, bodyy, w, h):
        self.space = space

        mass = 20

        torso = setup_body(space, bodyx+0, bodyy+h*3/8, mass*2, w, h*3/4, 1, 2)
        head = setup_body(space, bodyx+0, bodyy+h*7/8, mass/2.0, w/2, h/4, 1, 2)

        thighL = setup_body(space, bodyx-w/4.0, bodyy-h/4.0, mass, w/2.0, h/2.0, 2)
        thighR = setup_body(space, bodyx+w/4.0, bodyy-h/4.0, mass, w/2.0, h/2.0, 2)

        calfL = setup_body(space, bodyx-w/4.0, bodyy-h*3/4.0, mass, w/2.0, h/2.0, 2)
        calfR = setup_body(space, bodyx+w/4.0, bodyy-h*3/4.0, mass, w/2.0, h/2.0, 2)

        footL = setup_body(space, bodyx-w/4+w/8, bodyy-h*17/16, mass/2.0, w*3/4, h/8, 2)
        footR = setup_body(space, bodyx+w/4+w/8, bodyy-h*17/16, mass/2.0, w*3/4, h/8, 2)

        # Order determines draw order
        self.bodies = [load_sprite("thigh.png", thighR), 
                       load_sprite("calf.png", calfR), 
                       load_sprite("foot.png", footR), 
                       load_sprite("torso.png", torso), 
                       load_sprite("thigh.png", thighL), 
                       load_sprite("calf.png", calfL), 
                       load_sprite("foot.png", footL), 
                       load_sprite("head.png", head)]

        create_joint(space, torso,  head,   bodyx,       bodyy+h*3/4, -math.pi/10,  math.pi/10)
        create_joint(space, torso,  thighL, bodyx-w/4,   bodyy      , -math.pi*3/4, math.pi/2)
        create_joint(space, torso,  thighR, bodyx+w/4,   bodyy      , -math.pi*3/4, math.pi/2)
        create_joint(space, thighL, calfL,  bodyx-w/4.0, bodyy-h/2.0, -math.pi/2,  -math.pi/10 )
        create_joint(space, thighR, calfR,  bodyx+w/4.0, bodyy-h/2.0, -math.pi/2,  -math.pi/10)
        create_joint(space, calfL,  footL,  bodyx-w/4.0, bodyy-h    , -math.pi/10,  math.pi/10)
        create_joint(space, calfR,  footR,  bodyx+w/4.0, bodyy-h    , -math.pi/10,  math.pi/10)

        # save variables as members
        self.thighL = thighL
        self.thighR = thighR
        self.calfL = calfL
        self.calfR = calfR
        self.torso = torso

    def draw(self):
        for graphic in self.bodies:
            graphic.position = graphic.body.position
            graphic.rotation = -graphic.body.angle * 180 / math.pi
            graphic.draw()

    def get_position(self):
        return self.torso.position

    def reset(self):
        for sprite in self.bodies:
            sprite.body.position = sprite.body.start_position
            sprite.body.angle = 0

    def move_thighL(self, force=90):
        self.thighL.apply_impulse_at_local_point((force, 0), (0, 0))

    def move_thighR(self, force):
        self.thighR.apply_impulse_at_local_point((force, 0), (0, 0))

    def move_calfL(self, force):
        self.calfL.apply_impulse_at_local_point((-force, 0), (0, 0))

    def move_calfR(self, force):
        self.calfR.apply_impulse_at_local_point((-force, 0), (0, 0))

    def init_pose(self):
        pass

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

# https://pyglet.readthedocs.io/en/latest/modules/sprite.html
def load_sprite(name, body):
    image = pyglet.resource.image(name)                        
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    sprite = pyglet.sprite.Sprite(image)
    sprite.scale = body.height / (image.height)
    sprite.body = body
    return sprite
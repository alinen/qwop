"""
alinen 2020
Hello World pyglet application which tests events and sprites
"""

import pyglet
import time
import math
from pyglet.window import key

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

image = pyglet.resource.image('star.png')                        
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2
sprite = pyglet.sprite.Sprite(image, x = 200, y = 200)
fps_display = pyglet.window.FPSDisplay(window=window)
elapsedTime = 0

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.ENTER:
        print('The enter key was pressed.')
    elif symbol == key.ESCAPE:
        window.close()
        
@window.event
def on_draw():
    window.clear()
    label.draw()
    sprite.draw()
    fps_display.draw()

def update(dt):
    global elapsedTime
    elapsedTime += dt
    print(elapsedTime)
    sprite.rotation = elapsedTime * 10
    sprite.scale = math.sin(elapsedTime)

pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()

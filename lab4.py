import glfw
from OpenGL.GL import *
import math
import random

W, H = 800, 600

def draw_pixel(x, y):
    glVertex2f(x, y)

def draw8way(xc, yc, x, y):
    draw_pixel(xc + x, yc + y)
    draw_pixel(xc + x, yc - y)
    draw_pixel(xc - x, yc + y)
    draw_pixel(xc - x, yc - y)
    draw_pixel(xc + y, yc + x)
    draw_pixel(xc + y, yc - x)
    draw_pixel(xc - y, yc + x)
    draw_pixel(xc - y, yc - x)

def drawCircle(r, xc, yc, color):
    glColor3ub(*color)
    d = 5 - 4 * r
    x = 0
    y = r
    draw8way(xc, yc, x, y)
    while abs(x) < abs(y):
        if d < 0:
            d += -8 * x + 12
        else:
            d += -8 * x - 8 * y + 20
            y = y - 1
        x = x - 1
        draw8way(xc, yc, x, y)

def check_collision(circle1, circle2):
    distance = math.sqrt((circle1['xc'] - circle2['xc'])**2 + (circle1['yc'] - circle2['yc'])**2)
    combined_radius = circle1['r'] + circle2['r']
    return distance <= combined_radius

def myEvent(Window):
    circle1 = {'r': 50, 'xc': -100, 'yc': 0, 'tx': 2, 'ty': 1, 'color': [255, 0, 0]}
    circle2 = {'r': 50, 'xc': 100, 'yc': 0, 'tx': -1, 'ty': -2, 'color': [255, 0, 0]}

    while not glfw.window_should_close(Window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_POINTS)

        drawCircle(circle1['r'], circle1['xc'], circle1['yc'], circle1['color'])
        drawCircle(circle2['r'], circle2['xc'], circle2['yc'], circle2['color'])

        glEnd()

        for circle in [circle1, circle2]:
            circle['xc'] += circle['tx']
            circle['yc'] += circle['ty']

            if (circle['xc'] + circle['r']) > (W / 2 - 1) or (circle['xc'] - circle['r']) < (-W / 2):
                circle['tx'] *= -1

            if (circle['yc'] + circle['r']) > (H / 2 - 1) or (circle['yc'] - circle['r']) < (-H / 2):
                circle['ty'] *= -1

        # Check collision and reverse directions if needed
        if check_collision(circle1, circle2):
            circle1['tx'] *= -1
            circle1['ty'] *= -1
            circle2['tx'] *= -1
            circle2['ty'] *= -1

        glfw.swap_buffers(Window)
        glfw.poll_events()

    glfw.terminate()

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    Window = glfw.create_window(W, H, "Lab 4", None, None)
    if not Window:
        glfw.terminate()
        return

    glfw.make_context_current(Window)

    # Set up the orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W / 2, W / 2 - 1, -H / 2, H / 2 - 1, -1, 1)

    # Set up to use the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    myEvent(Window)  # line drawing

    glfw.terminate()

main()

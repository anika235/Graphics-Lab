# Anika Tabassum
#Roll 61
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

colors = [
    [255, 255, 255],
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 0],
    [0, 255, 255],
    [255, 0, 255],
    [127, 127, 127]
]

def get_zone(x1, x2, y1, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx >= 0 and dy >= 0:
        if dx > dy:
            return 0
        return 1
    elif dx >= 0 and dy < 0:
        if abs(dx) > abs(dy):
            return 7
        return 6
    elif dx < 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 3
        return 2
    else:
        if abs(dx) > abs(dy):
            return 4
        return 5

def convert_back(zone, x, y):
    if zone == 0:
        return -y, x
    elif zone == 1:
        return x, -y
    elif zone == 2:
        return -x, -y
    elif zone == 3:
        return y, x
    elif zone == 4:
        return y, -x
    elif zone == 5:
        return -x, y
    elif zone == 6:
        return x, y
    else:
        return -y, -x

def convert_to_6(zone, x, y):
    if zone == 0:
        return y, -x
    elif zone == 1:
        return x, -y
    elif zone == 2:
        return -x, -y
    elif zone == 3:
        return y, x
    elif zone == 4:
        return -y, x  # Corrected transformation
    elif zone == 5:
        return -x, y
    elif zone == 6:
        return x, y
    else:
        return -y, -x

def draw_axes():
    glBegin(GL_LINES)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-400, 0)
    glVertex2f(400, 0)

    # Y axis in green
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(0, -300)
    glVertex2f(0, 300)
    glEnd()

def draw_pixel(x, y, zone):
    glColor3ub(colors[zone][0], colors[zone][1], colors[zone][2])
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line_6(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = 2 * dx + dy
    del_s = 2 * dx
    del_se = 2 * (dx + dy)
    while y > y1:
        conx, cony = convert_back(zone, x, y)
        draw_pixel(int(conx), int(cony), zone)
        if d < 0:
            d += del_s
            y -= 1
        else:
            d += del_se
            x += 1
            y -= 1

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Lab 3", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up the orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-400, 400, -300, 300)
    
    # Set up to use the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_axes()

    n = int(input("Angle: "))
    r = int(input("Radius: "))
    
    lines = 360 / n
    theta = 0
    for it in range(int(lines)):
        x1 = 0
        y1 = 0
        x2 = r * math.cos(math.radians(theta))
        y2 = r * math.sin(math.radians(theta))
        zone = get_zone(x1, x2, y1, y2)
        dx, dy = convert_to_6(zone, x2 - x1, y2 - y1)
        draw_line_6(0, 0, dx, dy, zone)
        theta += n

    glfw.swap_buffers(window)
    glfw.poll_events()
    while not glfw.window_should_close(window):
        glfw.wait_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

import glfw
from OpenGL.GL import *
import math

W, H = 800, 600

colors = [[255, 255, 255],
          [255, 0, 0],
          [0, 255, 0],
          [0, 0, 255],
          [255, 255, 0],
          [0, 255, 255],
          [255, 0, 255],
          [127, 127, 127]]


def draw_axes():
    glColor3ub(127, 127, 127)
    glBegin(GL_LINES)
    glVertex2f(-W / 2, 0)
    glVertex2f(W / 2 - 1, 0)
    glVertex2f(0, -H / 2)
    glVertex2f(0, H / 2 - 1)
    glEnd()


def draw_pixel(x, y):
    glVertex2f(x, y)


def draw8way(xc, yc, x, y):
    draw_pixel(xc + x, yc + y)
    draw_pixel(xc - x, yc + y)
    draw_pixel(xc + x, yc - y)
    draw_pixel(xc - x, yc - y)
    draw_pixel(xc + y, yc + x)
    draw_pixel(xc - y, yc + x)
    draw_pixel(xc + y, yc - x)
    draw_pixel(xc - y, yc - x)


def drawCircle(r, xc, yc):
    d = 1 - r
    x = 0
    y = r

    while (abs(x) <= abs(y)):
        if d > 0:
            y = y-1
            d = d - 2 * x - 2 * y + 5
        else:
            d = d - 2 * x + 3 
        x = x-1
        draw8way(xc, yc, x, y)
        print(x,y)


def myEvent():
    r = int(input("Enter radius: "))
    xc = int(input("Enter x-coordinate of the center: "))
    yc = int(input("Enter y-coordinate of the center: "))
    glBegin(GL_POINTS)
    drawCircle(r, xc, yc)
    glEnd()


def main():
    if not glfw.init():
        return

    Window = glfw.create_window(W, H, "Lab 3", None, None)
    if not Window:
        glfw.terminate()
        return

    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W / 2, W / 2 - 1, -H / 2, H / 2 - 1, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_axes()  
    myEvent()  

    glfw.swap_buffers(Window)
    glfw.poll_events()

    while not glfw.window_should_close(Window):
        glfw.wait_events()

    glfw.terminate()


main()

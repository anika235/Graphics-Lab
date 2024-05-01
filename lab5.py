import glfw
from OpenGL.GL import *
import math
import random

W, H = 800, 600

colors= [
[255,255,255],
[255,0,0],
[0,255,0],
[0,0,255],
[255,255,0],
[0,255,255],
[255,0,255],
[127,127,127]]

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def get_zone(x0, y0, x1, y1):
    dx= x1-x0
    dy= y1-y0

    if dx>=0 and dy>=0:
        if dx > dy:
            return 0
        return 1

    elif dx>=0 and dy<0:
        if abs(dx) > abs(dy):
            return 7
        return 6

    elif dx<0 and dy>=0:
        if abs(dx) > abs(dy) :
            return 3
        return 2

    else:
        if abs(dx)>abs(dy):
            return 4
        return 5

def return_back(zone, x, y): 
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
        return -y, x  
    elif zone == 5:
        return -x, y
    elif zone == 6:
        return x, y
    else:
        return -y, -x

intersection = []

def draw_pixel(x, y, zone, ux, uy, bx, by):
    x, y = return_back(zone, x, y)
    if (x == ux):
        if by <= y and y <= uy:
            intersection.append((x, y))
    elif (x == bx):
        if by <= y and y <= uy:
            intersection.append((x, y))
    elif (y == uy):
        if bx <= x and x <= ux:
            intersection.append((x, y))
    elif (y == by):
        if bx <= x and x <= ux:
            intersection.append((x, y))
    glVertex2f(x, y)

def draw_line_6(x0, y0, x1, y1, zone, ux, uy, bx, by):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = 2 * dx + dy
    del_w = 2 * dx
    del_nw = 2 * (dx + dy)
    glBegin(GL_POINTS)
    draw_pixel(x, y, zone, ux, uy, bx, by)
    while (x<=x1):
        if (d < 0):
            d += del_w
            y -= 1
        else:
            d += del_nw
            x += 1
            y -= 1
        draw_pixel(x, y, zone, ux, uy, bx, by)
    glEnd()

def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):

    code0 = compute_code(x0, y0, xmin, ymin, xmax, ymax)
    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if code0 == 0 and code1 == 0:  # Both endpoints are inside the window
            return int(x0), int(y0), int(x1), int(y1)
        elif (code1 & code0) != 0:  # Both endpoints are outside the same region (on the same side of the window)
            return None, None, None, None
        else:
            code_out = code0 if code0 else code1

            if code_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif code_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif code_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif code_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin

            if code_out == code0:
                x0, y0 = x, y
                code0 = compute_code(x0, y0,  xmin, ymin, xmax, ymax)
            else:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)

def drawline(x0, y0, x1, y1, ux, uy, bx, by):
    zone = get_zone(x0, y0, x1, y1)
    x0, y0 = convert_to_6(zone, x0, y0)
    x1, y1 = convert_to_6(zone, x1, y1)
    draw_line_6(x0, y0, x1, y1, zone, ux, uy, bx, by)

def myEvent(n, ux, uy, bx, by):
    x0 = random.randint(-W // 2, W // 2)
    y0 = random.randint(-H // 2, H // 2)
    listforpoints = []
    for i in range(n):
        x1 = random.randint(-W // 2, W // 2)
        y1 = random.randint(-H // 2, H // 2)
        clipped_x0, clipped_y0, clipped_x1, clipped_y1 = cohen_sutherland_clip(x0, y0, x1, y1, bx, by, ux, uy)
        if clipped_x0 is not None:
            glColor3ub(255, 255, 0)
            drawline(clipped_x0, clipped_y0, clipped_x1, clipped_y1, ux, uy, bx, by)
            glColor3ub(128, 128, 128)
            drawline(x0, y0, clipped_x0, clipped_y0, ux, uy, bx, by)
            drawline(clipped_x1, clipped_y1, x1, y1, ux, uy, bx, by)
        else:
            glColor3ub(128, 128, 128)
            drawline(x0, y0, x1, y1, ux, uy, bx, by)
        listforpoints.append((x0, y0))
        x0, y0 = x1, y1
    glPointSize(5)
    glBegin(GL_POINTS)
    for (x, y) in listforpoints:
        glVertex2f(x, y)
    glEnd()
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3ub(255, 0, 0)
    for (x, y) in intersection:
        glVertex2f(x, y)
    glEnd()

def main():
   
    ux, uy = map(int, input("Enter Xmin, Ymin: ").split())
    bx, by = map(int, input("Enter Xmax, Ymax: ").split())
    n = int(input("Enter the number of lines: "))
    if not glfw.init():
        return
    

    Window = glfw.create_window(W, H, "Lab 5", None, None)
    if not Window:
        glfw.terminate()
        return

    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glBegin(GL_LINE_LOOP)
    glVertex2f(-W // 2, by)
    glVertex2f(W // 2, by)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glVertex2f(-W // 2, uy)
    glVertex2f(W // 2, uy)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glVertex2f(bx, -H // 2)
    glVertex2f(bx, H // 2)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glVertex2f(ux, -H // 2)
    glVertex2f(ux, H // 2)
    glEnd()
    myEvent(n, bx, by, ux, uy)

    glfw.swap_buffers(Window)
    glfw.poll_events()

    while not glfw.window_should_close(Window):
        glfw.wait_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
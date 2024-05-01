import glfw
from OpenGL.GL import *
import math
import random
import numpy as np

W, H = 800, 600
Window = None
MODE = 0

class Edge:
    def __init__(self, ymin, ymax, x, slope_inverse, x1, y1, x2, y2):
        self.ymin = ymin
        self.ymax = ymax
        self.x = x
        self.slope_inverse = slope_inverse
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

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
    
def allZone_to_6(zone, x, y): 
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

def draw_pixel(x, y, zone):
    x, y = return_back(zone, x, y)
    glVertex2f(x, y)

def draw_line_6(x0, y0, x1, y1, zone): 
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = 2 * dx + dy
    del_w = 2 * dx
    del_nw = 2 * (dx + dy)
    draw_pixel(x, y, zone)
    while (x<=x1 and y>=y1):
        if (d < 0):
            d += del_w
            y -= 1
        else:
            d += del_nw
            x += 1
            y -= 1
        draw_pixel(x, y, zone)

def inputfromfile(filename):
    points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                x, y = map(int, line.strip().split(','))
                points.append((x, y))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except ValueError:
        print(f"Error: Invalid format in '{filename}'.")
        return None
    return points

def alledges(vertices):
    all_edges = []
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        if y1 != y2:
            if y1 > y2:
                ymin, ymax = y2, y1
                x = x2
            else:
                ymin, ymax = y1, y2
                x = x1      
            slope_inverse = (x2 - x1) / (y2 - y1)
            all_edges.append(Edge(ymin, ymax, x, slope_inverse, x1, y1, x2, y2))
    return all_edges

def edgestable(all_edges):
    global_edgetable = []
    for edge in all_edges:
        index = 0
        for i, current_edge in enumerate(global_edgetable):
            if edge.ymin < current_edge.ymin:
                break
            elif edge.ymin == current_edge.ymin and edge.x < current_edge.x:
                break
            index += 1
        global_edgetable.insert(index, edge)
    return global_edgetable

def initialize_active_edge_table(scanline, global_edgetable):
    active_edge_table = []
    for edge in global_edgetable:
        if edge.ymin == scanline:
            active_edge_table.append(edge)
        elif edge.ymin > scanline:
            break
    return active_edge_table

def fill_polygon(vertices):
    all_edges = alledges(vertices)
    global_edgetable = edgestable(all_edges)
    scanline = global_edgetable[0].ymin
    active_edge_table = initialize_active_edge_table(scanline, global_edgetable)
    for edge in active_edge_table:
        global_edgetable.remove(edge)
    glColor3ub(255, 255, 255)
    glBegin(GL_POINTS)
    while active_edge_table:
        for i in range(0, len(active_edge_table), 2):
            edge1 = active_edge_table[i]
            edge2 = active_edge_table[i + 1]
            x1 = int(edge1.x)
            x2 = int(edge2.x)
            for x in range(x1, x2 + 1):
                glVertex2f(int(x), int(scanline))
        scanline += 1
        active_edge_table = [edge for edge in active_edge_table if edge.ymax != scanline]
        for edge in active_edge_table:
            edge.x += edge.slope_inverse
        add_edges = [edge for edge in global_edgetable if edge.ymin <= scanline]
        if add_edges:
            active_edge_table.extend(add_edges)
            for edge in add_edges:
                global_edgetable.remove(edge)
        remove_edges = [edge for edge in active_edge_table if scanline >= edge.ymax]
        for edge in remove_edges:
            active_edge_table.remove(edge)
        active_edge_table.sort(key=lambda edge: edge.x)
    glEnd()

def rotation_matrix(angle):
    theta = np.radians(angle)
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]])

def rotate_points(points, center, angle):
    points = np.array(points)
    center = np.array(center)
    translated_points = points - center
    rotated_points = np.dot(translated_points, rotation_matrix(angle))
    rotated_points += center
    return rotated_points.tolist()

def calculate_area(vertices):
    area = 0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

def calculate_centroid(vertices):
    area = calculate_area(vertices)
    cx = cy = 0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        factor = x1 * y2 - x2 * y1
        cx += (x1 + x2) * factor
        cy += (y1 + y2) * factor
    cx /= 6 * area
    cy /= 6 * area
    return (cx, cy)

def myEvent(points, Window):
    global MODE
    n = len(points)
    center = calculate_centroid(points)
    angle = 5.0
    if glfw.get_key(Window, glfw.KEY_1) == glfw.PRESS :
        MODE = 1
    elif glfw.get_key(Window, glfw.KEY_0) == glfw.PRESS :
        MODE = 0
    elif glfw.get_key(Window, glfw.KEY_2) == glfw.PRESS :
        MODE = 2
    elif glfw.get_key(Window, glfw.KEY_RIGHT):
        points = rotate_points(points, center, angle)
    elif glfw.get_key(Window, glfw.KEY_LEFT):
        points = rotate_points(points, center, -angle)
    
    if MODE == 1:
        glColor3ub(255, 255, 255)  
        glPointSize(1.0)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            zone = get_zone(x0, y0, x1, y1)
            dx0, dy0 = allZone_to_6(zone, x0, y0)
            dx1, dy1 = allZone_to_6(zone, x1, y1)
            glBegin(GL_POINTS)
            draw_line_6(dx0, dy0, dx1, dy1, zone)
            glEnd()
    elif MODE == 0:
        glColor3ub(255, 255, 255)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for (x, y) in points:
            glVertex2f(x,y)
        glEnd()

    elif MODE == 2:
        fill_polygon(points)
    return points

def main():
    print("Press 0, 1 and 2 = vertex only, boundary-pixel and filled polygon")
    print("Press  Right-arrow = rotate polygon -5 degree with center of rotation is isocenter of the polygon and Left arrow = opposite.")
   
    if not glfw.init():
        return
    
    Window = glfw.create_window(W, H, "Lab 6", None, None)
    if not Window:
        glfw.terminate()
        return
    
    glfw.set_input_mode(Window,glfw.STICKY_KEYS,GL_TRUE) 

    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    points = inputfromfile("points.txt")
    if points is None:
        return


    while not glfw.window_should_close(Window):
        glfw.wait_events()

        glClear(GL_COLOR_BUFFER_BIT)

        points = myEvent(points, Window)  

        glfw.swap_buffers(Window)

    glfw.terminate()

if __name__ == "__main__":
    main()

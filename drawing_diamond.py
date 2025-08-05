from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 
import random
import math

window_width, window_height = 500, 500
dmd_common_x = random.randrange(-window_width//2 + 50, window_width//2-31)
dmd_common_y = 230
x2 = dmd_common_x - 25
x3 = dmd_common_x + 25
y2 = dmd_common_y - 25
y3 = dmd_common_y - 50

class mid_point_line_drawing:

    def __init__ (self, start_x, start_y, end_x, end_y):
        self.x1 = start_x
        self.y1 = start_y
        self.x2 = end_x
        self.y2 = end_y

    def find_zone(self):
        zone = 0

        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        if abs(dx) == dx and abs(dy) == dy:
            if dx < dy:
                zone = 1
        elif abs(dx) != dx and abs(dy) == dy:
            if dx > dy:
                zone = 3
            else:
                zone = 2
        elif abs(dx) != dx and abs(dy) != dy:
            if dx > dy:
                zone = 4
            else:
                zone = 5
        else:
            if dy > dx:
                zone = 6
            else:
                zone = 7

        return zone

    def zone_shifter(self, zone):
        if zone == 1:
            self.x1, self.y1 = self.y1, self.x1
            self.x2, self.y2 = self.y2, self.x2
        elif zone == 2: 
            self.x1, self.y1 = self.y1, (self.x1)*(-1)
            self.x2, self.y2 = self.y2, self.x2*(-1)
        elif zone == 3: 
            self.x1, self.y1 = self.x1*(-1), self.y1
            self.x2, self.y2 = self.x2*(-1), self.y2
        elif zone == 4:
            self.x1, self.y1 = self.x1*(-1), self.y1*(-1)
            self.x2, self.y2 = self.x2*(-1), self.y2*(-1)
        elif zone == 5:
            self.x1, self.y1 = self.y1*(-1), self.x1*(-1)
            self.x2, self.y2 = self.y2*(-1), self.x2*(-1)
        elif zone == 6:
            self.x1, self.y1 = self.y1*(-1), self.x1
            self.x2, self.y2 = self.y2*(-1), self.x2
        elif zone == 7:
            self.x1, self.y1 = self.x1, self.y1*(-1)
            self.x2, self.y2 = self.x2, self.y2*(-1)
    
    def revrese_zone_shift(self, x1, y1, zone):
        if zone == 1:
            x1, y1 = y1, x1
        elif zone == 2: 
            x1, y1 = y1*(-1), (x1)
        elif zone == 3: 
            x1, y1 = x1*(-1), y1
        elif zone == 4:
            x1, y1 = x1*(-1), y1*(-1)
        elif zone == 5:
            x1, y1 = y1*(-1), x1*(-1)
        elif zone == 6:
            x1, y1 = y1, x1*(-1)
        elif zone == 7:
            x1, y1 = x1, y1*(-1)

        return (x1, y1)

    def finding_pixels(self):
        pixel_list = []

        zone = self.find_zone()
        self.zone_shifter(zone)
        x1, y1 = self.revrese_zone_shift(self.x1, self.y1, zone)
        pixel_list.append((x1, y1))
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        d = 2*abs(dy) - abs(dx)

        num_iteration = max(abs(dx), abs(dy))

        for i in range(num_iteration+1):
            if d < 0:
                if abs(dx) == dx:
                    self.x1+=1
                elif abs(dx) != dx:
                    self.x1-=1
                
                d = d + (2*dy)
            
            else:
                if abs(dx) == dx and abs(dy) == dy:
                    self.x1+=1
                    self.y1+=1
                elif abs(dx) != dx and abs(dy) != dy:
                    self.x1-=1
                    self.y1-=1
                elif abs(dx) != dx and abs(dy) == dy:
                    self.x1-=1
                    self.y1+=1
                else:
                    self.x1+=1
                    self.y1-=1

                d = d + 2*(dy - dx)

            x1, y1 = self.revrese_zone_shift(self.x1, self.y1, zone)
            pixel_list.append((x1, y1))

        return pixel_list
    
class drawing_line:

    def __init__(self, pixel_list):
        self.pixels = pixel_list

    def draw_points(self, x, y):
        glPointSize(5) 
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_line(self):
        for i in self.pixels:
            x, y = i

            x = int(x*math.cos(45) - y*math.sin(45))
            y = int(x*math.sin(45) + y*math.cos(45))
        
            self.draw_points(x, y)

# class diamond:

#     def draw_square(self):
#         global dmd_common_x, dmd_common_y

#         mpl_algorithm = mid_point_line_drawing(-2, 4, -3, -5)
#         pixel_list = mpl_algorithm.finding_pixels()

#         lets_draw_line = drawing_line()
#         for i in pixel_list:
#             x, y = i
#             lets_draw_line.draw_points(x, y)

#         glutSwapBuffers()

def display():
    global dmd_common_x, dmd_common_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    mpl_algorithm = mid_point_line_drawing(dmd_common_x - 50, dmd_common_y - 50, dmd_common_x, dmd_common_y)
    pixel_list = mpl_algorithm.finding_pixels()
    lets_draw_line = drawing_line(pixel_list)
    lets_draw_line.draw_line()

    # pixel_list = pixel_list.clear()
    # mpl_algorithm = mid_point_line_drawing(dmd_common_x, dmd_common_y + 1, dmd_common_x + 30, dmd_common_y + 1)
    # pixel_list = mpl_algorithm.finding_pixels()
    # lets_draw_line = drawing_line(pixel_list)
    # lets_draw_line.draw_line()

    # pixel_list = pixel_list.clear()
    # mpl_algorithm = mid_point_line_drawing(dmd_common_x, dmd_common_y - 30, dmd_common_x, dmd_common_y)
    # pixel_list = mpl_algorithm.finding_pixels()
    # lets_draw_line = drawing_line(pixel_list)
    # lets_draw_line.draw_line()

    # pixel_list = pixel_list.clear()
    # mpl_algorithm = mid_point_line_drawing(dmd_common_x + 31, dmd_common_y - 30, dmd_common_x + 31, dmd_common_y)
    # pixel_list = mpl_algorithm.finding_pixels()
    # lets_draw_line = drawing_line(pixel_list)
    # lets_draw_line.draw_line()

    glutSwapBuffers()

def init():
    global window_width, window_height

    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window_width/2, window_width/2, -window_height/2, window_height/2)
    glMatrixMode(GL_MODELVIEW)
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

window = glutCreateWindow(b'Game')

init()
glutDisplayFunc(display)

glutMainLoop() 
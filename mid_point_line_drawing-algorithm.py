from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

window_width, window_height = 500, 500

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
        elif zone == 2 and zone == 7: 
            self.x1, self.y1 = self.y1, (self.x1)*(-1)
            self.x2, self.y2 = self.y2, self.x2*(-1)
        elif zone == 3 or zone == 6: 
            self.x1, self.y1 = self.x1*(-1), self.y1
            self.x2, self.y2 = self.x2*(-1), self.y2
        elif zone == 4:
            self.x1, self.y1 = self.x1*(-1), self.y1*(-1)
            self.x2, self.y2 = self.x2*(-1), self.y2*(-1)
        elif zone == 5:
            self.x1, self.y1 = self.y1*(-1), self.x1*(-1)
            self.x2, self.y2 = self.y2*(-1), self.x2*(-1)
    
    def revrese_zone_shift(self, x1, y1, zone):
        if zone == 1:
            x1, y1 = y1, x1
        elif zone == 2 and zone == 7: 
            x1, y1 = y1, (x1)*(-1)
        elif zone == 3 or zone == 6: 
            x1, y1 = x1*(-1), y1
        elif zone == 4:
            x1, y1 = x1*(-1), y1*(-1)
        elif zone == 5:
            x1, y1 = y1*(-1), x1*(-1)

    def line_drawing(self):
        pixel_list = []

        zone = self.find_zone()
        self.zone_shifter(zone)
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        d = 2*dy - dx
        
  

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    mpl_algorithm = mid_point_line_drawing(-2, 4, -3, -5)
    mpl_algorithm.line_drawing()

    glutSwapBuffers()

def init():
    global window_width, window_height

    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

window = glutCreateWindow(b'Game')

init()
glutDisplayFunc(display)

glutMainLoop() 
from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

window_width, window_height = 500, 500
zone = 0

class mid_point_line_drawing:
    # global zone
    def __init__ (self, start_x, start_y, end_x, end_y):
        self.x1 = start_x
        self.y1 = start_y
        self.x2 = end_x
        self.y2 = end_y

    def find_zone(self):
        global zone

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
        
        

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

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
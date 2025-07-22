from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w_width, w_height = 500, 500


class createDot:
    def draw(self):
        global w_width, w_height 

        R = random.random()
        G = random.random()
        B = random.random()

        vertex_x = random.randint(0, 500)
        vertex_y = random.randint(0, 500)

        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3f(R, G, B)
        glVertex2f(vertex_x, vertex_y)
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    createDot().draw()

    glutSwapBuffers()

def init():
    glColor3f(1, 1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000)

glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )

window = glutCreateWindow(b'Magic Box')
init()

glutDisplayFunc(display)


glutMainLoop()
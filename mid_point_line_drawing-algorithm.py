from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

window_width, window_height = 500, 500

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
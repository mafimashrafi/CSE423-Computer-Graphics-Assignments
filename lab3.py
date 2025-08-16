from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

Grid_lentgh = 600

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    glutSwapBuffers()

def init():
    glEnable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1000/800, 0.1, 1000) 
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 800)   
glutInitWindowPosition(100, 100)
window = glutCreateWindow(b"3D OpenGL Intro")
init()
glutDisplayFunc(display)

glutMainLoop()
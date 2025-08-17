from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

Grid_lentgh = 60
camera_pos = (0, 500, 500)
fovY = 120 

def draw_grid():
    global Grid_lentgh
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-Grid_lentgh, Grid_lentgh, 0)
    glVertex3f(0, Grid_lentgh, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-Grid_lentgh, 0, 0)

    glVertex3f(Grid_lentgh, -Grid_lentgh, 0)
    glVertex3f(0, -Grid_lentgh, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(Grid_lentgh, 0, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-Grid_lentgh, -Grid_lentgh, 0)
    glVertex3f(-Grid_lentgh, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -Grid_lentgh, 0)

    glVertex3f(Grid_lentgh, Grid_lentgh, 0)
    glVertex3f(Grid_lentgh, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, Grid_lentgh, 0)
    glEnd()


def camera_setup():
    global camera_pos, fovY, Grid_lentgh
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1000/800, 0.1, 1000) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_pos
    gluLookAt(x, y, z, 
              0, 0, 0, 
              0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    camera_setup()

    for i in range(10):
        for j in range(10):
            glPushMatrix()
            glTranslatef(i * Grid_lentgh, j * Grid_lentgh, 0)
            draw_grid()
            glPopMatrix()
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